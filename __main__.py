"""
Initial python code.
Example of commenting
"""
from socket import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def get_mail_strings():
    prompts = ["Sender email (TA email): ",
               "Recipient email (student email): ",
               "Message subject: ",
               "Message body (finish with a separate line with a single period): "]

    inputs = []

    for i in range(len(prompts)):
        print(prompts[i])
        if i == 3:
            while inputs[len(inputs) - 1] != ".":
                input1 = str(input())
                """
                if input1 == ".":)
                    inputs.append('.')
                """
                inputs.append(input1)


        else:
            inputs.append(str(input()))  # TODO: Add some input validation here.

    return inputs


def string_split(text, delimiter):
    return text.split(delimiter, len(text))


def mime_message():
    img_filepath = 'verification_screenshot.jpg'
    with open(img_filepath, 'rb') as f:
        img_data = f.read()

    strings = get_mail_strings()
    msg = MIMEMultipart()
    msg['From'] = strings[0]
    msg['To'] = strings[1]
    msg['Subject'] = strings[2]

    jpg_part = MIMEApplication(img_data)
    jpg_part.add_header('Content-Disposition', 'attachment', filename='proof.jpg')
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
    # strings = get_mail_strings()
    msg = mime_message()

    mail_server = 'smtp2.bhsi.xyz'
    server_port = 2525

    line_terminator = '\r\n'

    # Mail content
    """
    ta_email = strings[0]  # 's171242@student.dtu.dk'
    rcpt_email = strings[1]
    subject = strings[2]
    mail_header = ['From: ' + ta_email + '\r\n',
                   'To: ' + rcpt_email + '\r\n',
                   'Subject:' + subject + '\r\n',
                   '\r\n']

    mail_body = []

    for i in range(len(strings) - 3):
        print(i)
        mail_body.append(strings[i + 3])
        mail_body.append(line_terminator)
    """

    msg_lines = string_split(msg.as_string(), '\0')

    print(msg_lines)
    # Establish TCP connection to mail_server
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

    """
    for line in mail_header:
        client_socket.send(line.encode())

    for line in mail_body:
        client_socket.send(line.encode())
    """

    receive = client_socket.recv(1024).decode()

    if receive[:3] != '250':
        print('250 reply not received from server.')
        client_socket.close()
        return

    print("Mail body successfully sent to mailserver.")
    """
    client_socket.send('QUIT\r\n'.encode())

    receive = client_socket.recv(1024).decode()

    if receive[:3] != '221':
        print('221 reply not received from server.')
        client_socket.close()
        return
    """
    print("Ended session with mailserver, closing socket.")

    client_socket.close()


if __name__ == "__main__":
    main()
