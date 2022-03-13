"""
Initial python code.
Example of commenting
"""
import socket
# import re
from socket import *
# import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
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

    if img_data != None:
        jpg_part = MIMEApplication(img_data)
        img_name = img_filepath.split('\\')
        jpg_part.add_header('Content-Disposition', 'attachment', filename = img_name[len(img_name)-1])
        msg.attach(jpg_part)

    msg_body = ''
    for i in range(len(strings) - 3):
        if i != len(strings) - 3:
            msg_body = msg_body + strings[i + 3] + '\r\n\0'
        else:
            msg_body = msg_body + strings[i + 3] + '\r\n'

    text = MIMEText(msg_body)
    msg.attach(text)

    return msg


def main():
    msg = mime_message()

    mail_server = 'smtp2.bhsi.xyz'
    server_port = 2525
    msg_lines = string_split(msg.as_string(), '\0')

    print(msg_lines)
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
