from socket import *


msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
#Fill in start
mailserver = 'smtp2.bhsi.xyz'
port = 2525
#Fill in end

# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, port))
#Fill in end

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO localhOst\r\n' # HEHLO for extended SMTP
clientSocket.send(heloCommand.encode()) 
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
# Fill in start
mailFromCommand = 'Mail From: <trump@gov.us>\r\n'
clientSocket.send(mailFromCommand.encode()) 
recv = clientSocket.recv(1024).decode()
print(recv)
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
RCPTCommand = 'RCPT TO: <goli@gmail.dk>\r\n'
clientSocket.send(RCPTCommand.encode()) 
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send DATA command and print server response.
# Fill in start
dataCommand = 'Data\r\n'
clientSocket.send(dataCommand.encode()) 
recv = clientSocket.recv(1024).decode()
print(recv)
# Fill in end

# Send message data.
# Fill in start
clientSocket.send(msg.encode())
# Fill in end

# Message ends with a single period.
# Fill in start
clientSocket.send(endmsg.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
# Fill in end

# Send QUIT command and get server response.
# Fill in start
quitCommand = 'Quit\r\n'
clientSocket.send(quitCommand.encode()) 
recv = clientSocket.recv(1024).decode()
print(recv)
# Fill in end



