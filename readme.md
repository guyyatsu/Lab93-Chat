# Lab-93 Socket-Based Communication System
This is a custom improvement on the basic socket-server chat system
everyone does in python at some point to get their feet wet; meant to
be integrated as an actual sub-system within the Lab-93 ecosystem.


## Upgraded Implementation
Some of the things being improved upon is synchronicity; the Lab-93 version
contains a database for storing messages while users are away from the client.

Another thing being introduced is in-line commands; by starting a message with
a forward slash character simple pre-defined commands can be executed:
  - ```/quit```: Exits the client.
  - ```/subject```: Attaches a subject to the message.


## Modes of Operation
There are two main use-cases of the chat system.  One is repeater mode, which operates
on a client/server model; and thenbroadcast mode, which creates a peer-to-peer network.

### Repeater Mode
Repeater mode sets up the system to act as a server that the client can
then connect to.  Useful if you want to self-host a chat room on your own
dedicated hardware.

### Broadcast Mode
Broadcast mode is used for chatting with other clients on the local network, i,e;
the client also acts as a server for everybody else on the sub-net while actively
searching for other servers on the net.
