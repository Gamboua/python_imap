import imaplib
import email
import re

from models import Message, session
from datetime import datetime
from dateutil import parser


class Imap:
    mail = None

    def __init__(self, date=None, origin=None, subject=None):
        self.date = date
        self.origin = origin
        self.subject = subject
    
    def get_date(self):
        return self.date

    def get_origin(self):
        return self.origin

    def get_subject(self):
        return self.subject

    def create_connection(self):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        
        user_email, user_pass = self.get_user_info()

        self.mail.login(user_email, user_pass)
        self.mail.select("inbox")

    def get_user_info(self):
        user_email = raw_input('Informe seu email (@gmail.com) : ')
        user_pass = raw_input('Informe sua senha : ')

        return [user_email, user_pass]

    def get_messages_list(self, word):
        self.create_connection()
        result, data = self.mail.search(None, '(OR BODY %s SUBJECT %s)' % (word, word))     

        return data[0].split()

    def fetch_message(self, position):
        result, data = self.mail.fetch(int(position), '(RFC822)')

        return email.message_from_string(data[0][1])

    def create_message_object(self, message):
        return Imap(
            date=message['Date'],
            origin=email.utils.parseaddr(message['From'])[1],
            subject=message['Subject']
        )

    def get_messages_by_body_subject(self, word):
        collection = [ 
            self.create_message_object(
                self.fetch_message(i)
            ) for i in self.get_messages_list(word)
        ]

        return collection

    
if __name__ == '__main__':
    obj = Imap()
    messages = obj.get_messages_by_body_subject('devops')

    for m in messages:
        try:
            mess = Message()
            data = parser.parse(m.get_date())
            mess.date = data
            mess.origin = m.get_origin()
            mess.origin = m.get_subject()

            session.add(mess)
            session.commit()
        except Exception as e:
            print(e)
