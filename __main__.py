"""
Initial python code.
Example of commenting
"""
import socket
from socket import *
import datetime

def main():
    mail_server = 'smtp2.bhsi.xyz'
    server_port = 2525

    # Mail content
    ta_email = 's171242@student.dtu.dk'
    rcpt_email = 's205460@dtu.dk'


    """
    current_time = datetime.datetime.now()
    print(current_time.strftime("%Y-%m-%d %H:%M:%S"))
    print(current_time)
    """

    mail_body = [
        "From: " + ta_email + "\r\n",
        "To: " + rcpt_email + "\r\n",
        "Subject: Whatever man vælger\r\n",
        "\r\n",
        "Tillykke med din nysendte email fra din TA.\r\n",
        "Hurra.\r\n",
        ".\r\n"
    ]

    # Establish TCP connection to mail_server
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((mail_server, server_port))

    receive = client_socket.recv(1024).decode()
    print(receive)

    if receive[:3] != '220':
        print('220 reply not received from server.')
        client_socket.close()
        return

    helo_command = 'HELO Alice\r\n'

    client_socket.send(helo_command.encode())

    receive = client_socket.recv(1024).decode()
    print(receive)

    if receive[:3] != '250':
        print('250 reply not received from server.')
        client_socket.close()
        return

    print('SMTP connection successfully established.')

    mail_from_command = 'MAIL FROM:<' + ta_email + '>\r\n'

    client_socket.send(mail_from_command.encode())

    receive = client_socket.recv(1024).decode()
    print(receive)

    if receive[:3] != '250':
        print('250 reply not received from server.')
        client_socket.close()
        return

    rcpt_command = 'RCPT TO:<' + rcpt_email + '>\r\n'

    client_socket.send(rcpt_command.encode())

    receive = client_socket.recv(1024).decode()
    print(receive)

    if receive[:3] != '250':
        print('250 reply not received from server.')
        client_socket.close()
        return

    client_socket.send('DATA\r\n'.encode())

    receive = client_socket.recv(1024).decode()
    print(receive)

    if receive[:3] != '354':
        print('354 reply not received from server.')
        client_socket.close()
        return

    for line in mail_body:
        client_socket.send(line.encode())

    receive = client_socket.recv(1024).decode()

    if receive[:3] != '250':
        print('250 reply not received from server.')
        client_socket.close()
        return

    print("Mail body successfully sent to mailserver.")

    client_socket.send('QUIT\r\n'.encode())

    receive = client_socket.recv(1024).decode()

    if receive[:3] != '221':
        print('221 reply not received from server.')
        client_socket.close()
        return

    print("Ended session with mailserver, closing socket.")

    client_socket.close()


if __name__ == "__main__":
    main()
