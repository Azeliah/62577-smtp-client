"""
Initial python code.
Example of commenting
"""
import os.path
import socket
# import re
import ssl
from socket import *
# import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import base64
# EMAIL: IDENTIFIER AT DOMAIN TLD
# TLD: [a-zA-Z]+
# DOMAIN: (([a-zA-Z0-9]+ (['-'|'_'][a-zA-Z]+)?)+ '.')+
# AT: '@'
# IDENTIFIER: ([a-zA-Z0-9]+ ['.'|'-'|'_'|'+']?)+
# ([a-zA-Z0-9]+ ['.'|'-'|'_'|'+']?)+ '@'(([a-zA-Z0-9]+ (['-'|'_'][a-zA-Z]+)?)+ '.')+ [a-zA-Z]+
# abcd   @  abc.com
# ab.cd  @  abc.com
# 1_2-3.a-b.c-d@a-b.c-d.co.uk


# def verify_email(email):



def get_mail_strings():
    prompts = ["Sender email (TA email): ",
               "Recipient email (student email): ",
               "Message subject: ",
               "Message body (finish with a separate line with a single period): ",
               "Attachment (filepath, or enter blank for no attachment): "]

    inputs = []

    for i in range(len(prompts)):
        print(prompts[i])
        if i == 3:
            while inputs[len(inputs) - 1] != ".":
                input1 = str(input())
                inputs.append(input1)

        else:
            inputs.append(str(input()))  # TODO: Add some input validation here.

    return inputs


def string_split(text, delimiter):
    return text.split(delimiter, len(text))


def mime_message():
    strings = get_mail_strings()
    img_filepath = strings[len(strings) - 1]
    try:
        with open(img_filepath, 'rb') as f:
            img_data = f.read()
    except FileNotFoundError:
        print('File cannot be found - no attachment included in email')
        img_data = None

    msg = MIMEMultipart()
    msg['From'] = strings[0]
    msg['To'] = strings[1]
    msg['Subject'] = strings[2]

    msg_body = ''
    for i in range(len(strings) - 5):
        msg_body = msg_body + strings[i + 3] + '\r\n\0'

    text = MIMEText(msg_body)
    msg.attach(text)

    if img_data is not None:
        jpg_part = MIMEApplication(img_data)
        jpg_part.add_header('Content-Disposition', 'attachment', filename = os.path.basename(img_filepath))
        msg.attach(jpg_part)

    return msg


def main():
    msg = mime_message()
    print(msg)
    msg_lines = string_split(msg.as_string(), '\0')

    mail_server = 'smtp.gmail.com' # 'smtp2.bhsi.xyz'
    server_port = 587 # 2525
    username = 'cxiao2305@gmail.com'
    pw = 'Group_05'

    # Establish TCP connection to mail_server
    """
    test_sock = socket(AF_INET, SOCK_STREAM)
    context = ssl.create_default_context()

    with test_sock.create_connection((mail_server, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=mail_server) as ssock:
            print(ssock.version())

    ssock.connect((mail_server, server_port))
    """

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((mail_server, server_port))

    receive = client_socket.recv(1024).decode()
    print(receive)

    if receive[:3] != '220':
        print('220 reply not received from server.')
        client_socket.close()
        return

    helo_command = 'EHLO Notalice\r\n'

    client_socket.send(helo_command.encode())

    receive = client_socket.recv(1024).decode()
    print(receive)

    if receive[:3] != '250':
        print('250 reply not received from server.')
        client_socket.close()
        return

    print('SMTP connection successfully established.')

    # Establish TLS connection
    TLS_command = 'STARTTLS\r\n'
    client_socket.send(TLS_command.encode())
    receive = client_socket.recv(1024).decode()
    print(receive)

    if receive[:3] != '220':
        print('220 reply not received from server.')
        client_socket.close()
        return

    client_socket = ssl.wrap_socket(client_socket)

    client_socket.send(helo_command.encode())
    receive = client_socket.recv(1024).decode()
    print(receive)

    # Authenticate
    command = 'AUTH LOGIN\r\n'
    client_socket.send(command.encode())
    receive = client_socket.recv(1024).decode()
    print(receive)

    username_base64 = base64.b64encode(username.encode("ascii"))
    pw_base64 = base64.b64encode(pw.encode("ascii"))

    client_socket.send(username_base64)
    client_socket.send('\r\n'.encode())
    receive = client_socket.recv(1024).decode()
    print(receive)

    client_socket.send(pw_base64)
    client_socket.send('\r\n'.encode())
    receive = client_socket.recv(1024).decode()
    print(receive)

    if receive[:3] != '235':
        print('235 reply not received from server.')
        client_socket.close()
        return

    mail_from_command = 'MAIL FROM:<' + msg['From'] + '>\r\n'

    client_socket.send(mail_from_command.encode())

    receive = client_socket.recv(1024).decode()
    print(receive)

    if receive[:3] != '250':
        print('250 reply not received from server.')
        client_socket.close()
        return

    rcpt_command = 'RCPT TO:<' + msg['To'] + '>\r\n'

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

    for line in msg_lines:
        client_socket.send(line.encode())
    client_socket.send("\r\n".encode())
    client_socket.send(".\r\n".encode())

    receive = client_socket.recv(1024).decode()

    if receive[:3] != '250':
        print('250 reply not received from server.')
        client_socket.close()
        return

    print("Mail body successfully sent to mailserver.")

    print("Ended session with mailserver, closing socket.")

    client_socket.close()


if __name__ == "__main__":
    main()
