import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List, Dict
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via SMTP"""
    
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        from_email: str,
        from_name: str = "MisMatch Platform"
    ):
        """Initialize email service
        
        Args:
            smtp_server: SMTP server address (e.g., smtp.gmail.com)
            smtp_port: SMTP server port (usually 587 for TLS)
            username: SMTP username
            password: SMTP password/app password
            from_email: Sender email address
            from_name: Sender display name
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.from_name = from_name
    
    def _create_message(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None
    ) -> MIMEMultipart:
        """Create email message with HTML and plain text alternatives
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_body: HTML email body
            text_body: Plain text email body (optional)
            
        Returns:
            MIMEMultipart message object
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = to_email
        message["Date"] = datetime.now().isoformat()
        
        # Attach plain text version
        if text_body:
            message.attach(MIMEText(text_body, "plain"))
        
        # Attach HTML version (preferred)
        message.attach(MIMEText(html_body, "html"))
        
        return message
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None
    ) -> bool:
        """Send an email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_body: HTML email body
            text_body: Plain text email body (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            message = self._create_message(to_email, subject, html_body, text_body)
            
            # Connect and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(message)
            
            logger.info(f"Email sent to {to_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_match_notification(
        self,
        to_email: str,
        candidate_name: str,
        job_title: str,
        match_score: float,
        explanation: str = ""
    ) -> bool:
        """Send match notification email
        
        Args:
            to_email: Recipient email
            candidate_name: Candidate name
            job_title: Job position
            match_score: Match score (0-1)
            explanation: Match explanation
            
        Returns:
            True if successful
        """
        html_body = f"""<html>
<body style="font-family: Arial, sans-serif;">
  <div style="max-width: 600px; margin: 0 auto;">
    <h1 style="color: #00aa00;">🎯 New Match Found!</h1>
    <p>Hi,</p>
    <p>We found a great match in our system:</p>
    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
      <tr style="background-color: #f0f0f0;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Candidate</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">{candidate_name}</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Job Position</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">{job_title}</td>
      </tr>
      <tr style="background-color: #f0f0f0;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Match Score</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>{match_score * 100:.1f}%</strong></td>
      </tr>
    </table>
    <p style="color: #333;">{explanation}</p>
    <a href="https://localhost:8000/dashboard" style="background-color: #00aa00; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View in Dashboard</a>
    <hr style="margin-top: 40px; border: none; border-top: 1px solid #ddd;">
    <p style="color: #666; font-size: 12px;">MisMatch Platform</p>
  </div>
</body>
</html>"""
        
        text_body = f"New Match: {candidate_name} for {job_title}\nScore: {match_score * 100:.1f}%"
        
        return self.send_email(
            to_email=to_email,
            subject=f"🎯 New Match: {candidate_name} → {job_title}",
            html_body=html_body,
            text_body=text_body
        )
    
    def send_daily_digest(
        self,
        to_email: str,
        metrics: Dict[str, any]
    ) -> bool:
        """Send daily digest email
        
        Args:
            to_email: Recipient email
            metrics: Dictionary with daily metrics
            
        Returns:
            True if successful
        """
        html_body = f"""<html>
<body style="font-family: Arial, sans-serif;">
  <div style="max-width: 600px; margin: 0 auto;">
    <h1 style="color: #4169e1;">📊 Daily Summary</h1>
    <p>Hi,</p>
    <p>Here's your daily summary:</p>
    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
      <tr style="background-color: #f0f0f0;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Total Matches</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">{metrics.get('total_matches', 0)}</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Success Rate</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">{metrics.get('success_rate', 0):.1f}%</td>
      </tr>
      <tr style="background-color: #f0f0f0;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Average Score</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">{metrics.get('avg_score', 0):.2f}</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Top Job</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">{metrics.get('top_job', 'N/A')}</td>
      </tr>
    </table>
    <a href="https://localhost:8000/dashboard" style="background-color: #4169e1; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Dashboard</a>
    <hr style="margin-top: 40px; border: none; border-top: 1px solid #ddd;">
    <p style="color: #666; font-size: 12px;">MisMatch Platform</p>
  </div>
</body>
</html>"""
        
        return self.send_email(
            to_email=to_email,
            subject="📊 Daily Summary Report",
            html_body=html_body
        )
    
    def send_weekly_report(
        self,
        to_email: str,
        report_data: Dict[str, any]
    ) -> bool:
        """Send weekly report email
        
        Args:
            to_email: Recipient email
            report_data: Weekly report data
            
        Returns:
            True if successful
        """
        html_body = f"""<html>
<body style="font-family: Arial, sans-serif;">
  <div style="max-width: 600px; margin: 0 auto;">
    <h1 style="color: #9c27b0;">📈 Weekly Report</h1>
    <p>Hi,</p>
    <p>Here's your weekly performance report:</p>
    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
      <tr style="background-color: #f0f0f0;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Metric</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Value</strong></td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;">Total Jobs Processed</td>
        <td style="padding: 10px; border: 1px solid #ddd;">{report_data.get('total_jobs', 0)}</td>
      </tr>
      <tr style="background-color: #f0f0f0;">
        <td style="padding: 10px; border: 1px solid #ddd;">Total Candidates Matched</td>
        <td style="padding: 10px; border: 1px solid #ddd;">{report_data.get('total_matches', 0)}</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;">Success Rate</td>
        <td style="padding: 10px; border: 1px solid #ddd;">{report_data.get('success_rate', 0):.1f}%</td>
      </tr>
    </table>
    <a href="https://localhost:8000/dashboard" style="background-color: #9c27b0; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Download Full Report</a>
    <hr style="margin-top: 40px; border: none; border-top: 1px solid #ddd;">
    <p style="color: #666; font-size: 12px;">MisMatch Platform</p>
  </div>
</body>
</html>"""
        
        return self.send_email(
            to_email=to_email,
            subject="📈 Weekly Performance Report",
            html_body=html_body
        )
    
    def send_password_reset(
        self,
        to_email: str,
        reset_link: str
    ) -> bool:
        """Send password reset email
        
        Args:
            to_email: Recipient email
            reset_link: Password reset link
            
        Returns:
            True if successful
        """
        html_body = f"""<html>
<body style="font-family: Arial, sans-serif;">
  <div style="max-width: 600px; margin: 0 auto;">
    <h1>Password Reset Request</h1>
    <p>Hi,</p>
    <p>Click the link below to reset your password:</p>
    <a href="{reset_link}" style="background-color: #ff9800; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a>
    <p style="color: #666; font-size: 12px;">This link expires in 24 hours.</p>
    <hr style="margin-top: 40px; border: none; border-top: 1px solid #ddd;">
    <p style="color: #666; font-size: 12px;">MisMatch Platform</p>
  </div>
</body>
</html>"""
        
        return self.send_email(
            to_email=to_email,
            subject="Password Reset Request",
            html_body=html_body
        )
