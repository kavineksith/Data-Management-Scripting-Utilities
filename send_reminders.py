#!/usr/bin/env python3

import datetime
import email.message
import smtplib
import sys

class EmailSendingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def create_message(date, title):
    message = email.message.EmailMessage()
    weekday = get_day_of_week(date)
    message['Subject'] = f'Meeting reminder: "{title}"'
    message.set_content(f'''
Hi all!
    
This is a quick mail to remind you all that we have a meeting about: "{title}"
on {weekday}, {date}.

See you there.
''')
    return message

def send_reminders(message, emails):
    try:
        smtp = smtplib.SMTP('localhost')
        message['From'] = 'noreply@example.com'
        for email in emails.split(','):
            del message['To']
            message['To'] = email.strip()
            smtp.send_message(message)
        smtp.quit()
        print("Successfully sent reminders to:", emails)
    except (smtplib.SMTPException, ConnectionError) as e:
        raise EmailSendingError(f"Failed to send email: {e}")

def get_day_of_week(date):
    dateobj = datetime.datetime.strptime(date, r"%Y-%m-%d")
    return dateobj.strftime("%A")

def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python send_reminders.py 'date|Meeting|Emails'")
            return 1

        meeting_info = sys.argv[1].split('|')
        if len(meeting_info) != 3:
            print("Invalid input format. Please use 'date|Meeting|Emails'.")
            return 1

        date, title, emails = meeting_info
        message = create_message(date, title)
        send_reminders(message, emails)
    except EmailSendingError as ese:
        print(f"Error sending email: {ese}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
