import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    """Email service for user notifications"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('SENDER_EMAIL', 'noreply@mismatch.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
    
    def send_verification_email(self, recipient_email, verification_link):
        """Send email verification link"""
        subject = "MisMatch - Verify Your Email"
        html_content = f"""
        <html>
            <body>
                <h2>Welcome to MisMatch!</h2>
                <p>Please verify your email by clicking the link below:</p>
                <a href="{verification_link}">Verify Email</a>
                <p>This link expires in 24 hours.</p>
            </body>
        </html>
        """
        self._send_email(recipient_email, subject, html_content)
    
    def _send_email(self, recipient, subject, html_content):
        """Internal method to send email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(html_content, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Email sending error: {str(e)}")
            return False
