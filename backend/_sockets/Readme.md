# Sockets
1. Not using Django channels because two way communication is difficult as send has to be called from inside django project
2. The `socket` library in python does not work as it is not designed for these purposes. Another library called `websockets` has been used for  creating a server.
3. There are two client files: One is in the angular pipeline.component.ts that uses Javascript sockets to connect to the server. Another file is `connect.py` that uses `websockets` for a client side program.

## Explanation of `sock.py`
In this file the main function is `counter` that coordinates everything. When a request is received , a `websocket` object is created for it. This added to the USERS set. 

Note that the way await works: It holds the execution for the particular function at the moment. So the execution is sequential for an async function, but two different async functions may be running in an interleaved fashion.

the line `for message in websocket` keeps on holding to the websocket. When the client disconnects, this loop ends and the `finally` part executes to deregister the user, which essentially is removing it from the set.

The notify functions are simple. They just send a message to a user and the message **has to be a string**. the syntax is obvious `user.send(message)`. One thing that I added differently: the user who had sent a message to the server does not receive it back. Rest all the users do.

The run_till_complete in the bottom basically run the function `counter` for all the users until all of them disconnect. So basically for each user, a different `counter` function is running.

The `connect.py` file contains the client program. It is pretty much self explanatory. The only thing is the careful use of async and await, that helps to run the program smoothly.