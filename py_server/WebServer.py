# Import socket module
import socket    

# Import sys module for argv
import sys

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Assign a port number
port = 12101
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    port = int(sys.argv[1])

# Bind the socket to server address and server port
newSocket.bind(('', port))

# Listen to at most 1 connection at a time
newSocket.listen(5)

# Server should be up and running and listening to the incoming connections
while True:
    print 'Ready to serve...'

    # Set up a new connection from the client
    conn, addr = newSocket.accept()

    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except clause is executed
    try:
        # Receives the request message from the client
        request = conn.recv(1024)
        if len(request) < 1:
            continue
        print(request)

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        parts = request.strip().split(' ')
        path = parts[1]

        # Because the extracted path of the HTTP request includes 
        # a character '\', we read the path from the second character 
        f = open(path[1:], 'r')

        # Store the entire contenet of the requested file in a temporary buffer
        page = f.read()

        # Send the HTTP response header line to the connection socket
        conn.send("HTTP/1.1 200 OK\r\n\r \n")
 
        # Send the content of the requested file to the connection socket
        conn.send(page)

        # Close the client connection socket
        conn.close()

    except IOError:
        # Send HTTP response message for file not found
        conn.send("HTTP/1.1 404 not found\r\n\r \n")

        # Close the client connection socket
        conn.close()

# Close the Server connection socket
newSocket.close()

