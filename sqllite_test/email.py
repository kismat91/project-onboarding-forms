import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, username='gamerpara111@gmail.com', password='nppo jcai srry oblc'):
        """Initialize the EmailSender with Gmail credentials."""
        self.username = username
        self.password = password
        self.server = None

    def connect(self):
        """Connect to the Gmail SMTP server."""
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()  # Secure the connection
        self.server.login(self.username, self.password)

    def send_email(self, recipient, subject, message):
        """Send an email to a specified recipient."""
        email = MIMEMultipart()
        email['From'] = self.username
        email['To'] = recipient
        email['Subject'] = subject
        email.attach(MIMEText(message, 'plain'))
        self.server.send_message(email)

    def close_connection(self):
        """Close the SMTP server connection."""
        if self.server:
            self.server.quit()

# Usage
if __name__ == "__main__":
    recipient = 'amitshendge1990@gmail.com'
    subject = 'Hello from Python'
    message = 'This is a test email sent from a Python script.'

    email_sender = EmailSender()
    try:
        email_sender.connect()
        email_sender.send_email(recipient, subject, message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        email_sender.close_connection()
