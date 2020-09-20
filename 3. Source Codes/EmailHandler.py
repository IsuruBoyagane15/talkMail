import smtplib
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
import imaplib
import email


class EmailHandler:

    # define static instance to keep singleton EmailHandler object
    __instance = None

    # static method to get EmailHandler instance
    @staticmethod
    def get_email_handler():
        if EmailHandler.__instance is None:
            EmailHandler()
        return EmailHandler.__instance

    # constructor
    def __init__(self):
        if EmailHandler.__instance is not None:
            raise Exception("A email handler instance has been already created...!")
        else:
            EmailHandler.__instance = self

    #verify user credentials
    def verify_user(self, email_address, password):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(email_address, password)
            return True
        except smtplib.SMTPAuthenticationError:
            return False
        except:
            return

    #send email
    def send_email(self , sender_email, password, message, user_name):

        if message['closure'] is not None:
            closure = message['closure'] + '\n' + user_name
        else:
            closure = user_name

        if message['content'] is not None:
            email_body = message['content'] + '\n\n\n--\n' + closure
        else:
            email_body = closure

        email_message = MIMEMultipart()
        email_message['From'] = sender_email
        email_message['To'] = message['to']
        email_message['Cc'] = message['cc']
        # email_message['Bcc'] = message['bcc']

        recipient_list = message['to'].split(',') + message['cc'].split(',') + message['bcc'].split(',')

        if message['subject'] != '':
            email_message['Subject'] = message['subject']

        email_message.attach(MIMEText(email_body, 'plain'))

        for i in message['attachments']:
            filename = i.split('/')[-1]
            attachment = open(i, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
            email.encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            email_message.attach(p)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(sender_email, password)
            text = email_message.as_string()
            server.sendmail(sender_email, recipient_list, text)
            server.quit()
            return True
        except:
            return False

    # load emails from the given mailbox
    def load_email(self, email_address, password, encryption_key, type):
        cipher_suite = Fernet(encryption_key)
        password = cipher_suite.decrypt(password).decode("utf-8")

        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(email_address, password)

            list_of_emails = []
            if type == 'inbox':
                mail.select('inbox')
            elif type == 'sentbox':
                mail.select('"[Gmail]/Sent Mail"')

            result, data = mail.uid('search', None, 'ALL')
            id_list = data[0].split()[::-1]

            if id_list:
                for email_id in id_list:

                    result, email_data = mail.uid('fetch', email_id, '(RFC822)')
                    raw_email = email_data[0][1].decode('utf-8')
                    email_message = email.message_from_string(raw_email)
                    if email_message.is_multipart():
                        # i = 0
                        for part in email_message.walk():
                            # i = i+1
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True)
                                body = body.decode(errors='ignore')

                            elif part.get_content_type() == "text/html":
                                continue
                    else:
                        body = email_message.get_payload()

                    email_details = {
                        'id': int(email_id),
                        'cc': email_message['Cc'],
                        'subject': email_message['Subject'],
                        'body': body
                    }
                    if type == 'inbox':
                        email_details['from'] = email_message['From']
                    elif type == 'sentbox':
                        email_details['to'] = email_message['To']
                        email_details['bcc'] = email_message['Bcc']

                    list_of_emails.append(email_details)
                mail.close()
                return list_of_emails
            else:
                mail.close()
                return False
        except:
            return 'con_error'
