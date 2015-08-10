# kivychat

This is a presentation on Kivy and some sample code to go with.  The sample code is a working XMPP chat client.

## Running the Code

You will need a working installation of Kivy 1.9 which creates its own virtualenv.  Inside of that virtualenv you
will need to install SleekXMPP

```sh
$ kivy pip install sleekxmpp==1.3.1
```

In order to connect to a chat server, the program expects a file named "storage.json" to contain host, port, username
and password information.  Example:

```javascript
{
    "account":{
        "userid":"foo@gmail.com",
        "password":"pa$$word"
    },
    "server":{
        "host":"talk.google.com",
        "port":5222
    }
}
```

Note that you can still use XMPP to talk to Google chat, but Google does all sorts of things to prevent you for security reasons.
You can work around them by explicitly changing your account settings: See 
[Not the end of XMPP for Google Talk](https://xmpp.org/2015/03/no-its-not-the-end-of-xmpp-for-google-talk/) and 
[Allowing less secure apps to access your account](https://support.google.com/accounts/answer/6010255)

You can then execute "main.py"

```sh
$ kivy main.py
```
