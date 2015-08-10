from Queue import Empty

from kivy.clock import Clock

from sleekxmpp import ClientXMPP

from friends import Friend

# ============================================================================
# GUI
# ============================================================================

class ChatClient(ClientXMPP):
    def __init__(self, root_box, userid, password):
        self.userid = userid
        self.root_box = root_box
        at_sign = userid.find('@')
        self.nick = userid[:at_sign]
        super(ChatClient, self).__init__(userid, password)
        self.message_count = 0

        # register some XMPP plug ins
        self.register_plugin('xep_0030')  # service discovery
        self.register_plugin('xep_0199')  # ping

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('no_auth', self.auth_failed)

        self.add_event_handler('got_online', self.status_change)
        self.add_event_handler('got_offline', self.status_change)
        self.add_event_handler('changed_status', self.status_change)
        self.add_event_handler('message', self.receive_chat)

        # register the callback trigger for when we receive a chat (processing
        # of chat has to happen on kivy's thread)
        self._chat_trigger = Clock.create_trigger(self._sync_receive_chat)

    def start(self, event):
        # retrieve our buddies and populate
        iq = self.get_roster()
        friends = []
        for key, value in iq['roster']['items'].items():
            friends.append(Friend(value['name'], key.bare, 'offline'))

        if friends:
            # we're connected and we have friends, get rid of the connection
            # label and insert the actual friend box
            self.root_box.ids.friend_box_container.clear_widgets()
            self.root_box.ids.friend_box_container.add_widget(
                self.root_box.friend_box)
            self.root_box.friend_box.add_friends(friends)
        else:
            self.root_box.ids.connection_label.text = ('Connected\n'
                'You have no friends')

        # tell the world we're here, this will also trigger getting our
        # friend's statuses back
        self.send_presence()

    def auth_failed(self, event):
        self.root_box.ids.connection_label.text = ('Connection Failed\n'
            'Check your settings')

    def status_change(self, event):
        status = event.get_type()
        who = event.get_from().bare
        if status == 'available':
            self.root_box.friend_box.change_status(who, 'online')
        elif status == 'unavailable':
            self.root_box.friend_box.change_status(who, 'offline')
        else:
            print '=> ignoring presence type of ', status

    def send_chat(self, msg_to, msg, mtype='chat'):
        msg = self.make_message(mto=msg_to, mbody=msg, mtype=mtype)
        self.message_count += 1
        msg['id'] = 'spakr%d' % self.message_count
        msg.send()

    def receive_chat(self, msg):
        """This call will happen on SleekXMPP's thread"""
        #print '==> rcvd:', msg
        if msg['type'] in ('chat', 'normal', ):
            self.root_box.receive_queue.put(msg)
            self._chat_trigger()

    def _sync_receive_chat(self, delta_time):
        """Should only be called by triggered event on kivy's thread to deal
        with any received messages."""
        try:
            while(True):
                # not an infinite loop, get() throws Empty
                msg = self.root_box.receive_queue.get(block=False)
                self._handle_chat_message(msg)
        except Empty:
            # nothing left to do
            pass

    def _handle_chat_message(self, msg):
        userid = msg.get_from().bare
        try:
            friend = self.root_box.friend_box.friend_rows[userid].friend
            self.root_box.chat_box.chat_received(friend, msg['body'])
            self.root_box.menu.show_item('Chats')

            # only increment the chat counter if the tab for this chat
            # isn't showing
            current_tab = self.root_box.chat_box.ids.tab_content.current
            if self.root_box.ids.screen_manager.current != 'Chats' \
                    or current_tab != friend.userid:
                friend.message_count += 1
        except KeyError:
            print '=> ignoring message from non-friend ', userid
