from socket import *
    

def main():
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
    # Fill in end

    # Send RCPT TO command and print server response.
    # Fill in start
    # Fill in end

    # Send DATA command and print server response.
    # Fill in start
    # Fill in end

    # Send message data.
    # Fill in start
    # Fill in end

    # Message ends with a single period.
    # Fill in start
    # Fill in end

    # Send QUIT command and get server response.
    # Fill in start
    # Fill in end


if __name__ == "__main__":
    main()
