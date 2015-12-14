Yasemin Alpay
BOUN SWE544 - Internet Programming Project
IRC-like Chat / Client Side

----------------------------------------------
2 main threads needed to for the Client-Side of the program:
These threads are ReadThread and WriteThread and they are started immediately
when the program starts. They are inherited from the "threading.Thread".
When the threads starts, the constructers and run(self, args[]) functions are called.
In both of the threads, there are loops inside run functions :
-ReadThread basically reads the information from a given socket in a loop.
-WriteThread writes to the socket and sends it to server in a loop.

**READ THREAD**
In ReadThread, there is an incoming_parser function.
This function is for parsing server responses and take actions with them. 
For example if server sends "ERL" signal to the client, it means that the 
user has not logged in yet and needs to select a nick to be able to chat.
The signals that are going to be sent by server are predefined. They can be
further examined in incoming_parser.

**CLIENT DIALOG**
ClientDialog runs when client starts,and it includes a function
named outgoing_parser. A user can enter some commands through client dialog screen.
These commands are parsed within this function and turned into 
the protocol signals. This way the server can understand what the user(client) means.

**WRITE THREAD**
The WriteThread sends the signals to the server from a given socket in a Queue. These signals comes from 
ClientDialog. If user directly types and enters to send the text, this string is transformed
to a signal that means the text will be sent to all users in the channel. (SAY signal)
In other cases, the string can mean different things, and they are parsed by given protocols.

**Queues**
All the signals that is written to and read from sockets are first put and get to a
sendQueue. At the meantime, all the strings that are going to be written and read from 
client dialog screen are again put and get to a screenQueue.
----------------------------------------------------
**BUGS**

-The private message doesn't work quite well.
-/quit action can be improved.
-There is no user list on the right side of the client dialog.


-------------------------------------------------------
**REPORTS on SERVER**
-The server that is used for tests does not support Turkish unicode characters.
-Server sends TIC signal periodically. If it collapses with the SAY signal, it sends them both.









 



