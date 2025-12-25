"""Email and SMS notification tasks."""

import logging
from typing import List, Dict, Any, Optional
from celery import shared_task
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.models import User, Notification
from app.services.health_check import log_service_operation
from app.config import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(
    self,
    recipient_email: str,
    subject: str,
    template: str,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Send email notification asynchronously.
    
    Args:
        recipient_email: Recipient email address
        subject: Email subject
        template: Email template name
        context: Template context variables
        
    Returns:
        Dict with email send result
    """
    try:
        start_time = datetime.utcnow()
        context = context or {}
        
        # Render email template
        html_body = _render_email_template(template, context)
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = recipient_email
        
        # Attach HTML content
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send via SMTP
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        # Log operation
        duration = (datetime.utcnow() - start_time).total_seconds()
        log_service_operation(
            service="notifications",
            operation="send_email",
            status="success",
            duration=duration,
            metadata={"recipient": recipient_email, "template": template}
        )
        
        logger.info(f"Email sent to {recipient_email} using template {template}")
        return {"status": "success", "recipient": recipient_email}
        
    except Exception as exc:
        logger.error(f"Error sending email to {recipient_email}: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_sms(
    self,
    phone_number: str,
    message: str
) -> Dict[str, Any]:
    """
    Send SMS notification asynchronously.
    
    Args:
        phone_number: Recipient phone number
        message: SMS message content
        
    Returns:
        Dict with SMS send result
    """
    try:
        start_time = datetime.utcnow()
        
        # Use Twilio API for SMS
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        message_obj = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        # Log operation
        duration = (datetime.utcnow() - start_time).total_seconds()
        log_service_operation(
            service="notifications",
            operation="send_sms",
            status="success",
            duration=duration,
            metadata={"phone": phone_number}
        )
        
        logger.info(f"SMS sent to {phone_number}")
        return {"status": "success", "phone": phone_number, "message_id": message_obj.sid}
        
    except Exception as exc:
        logger.error(f"Error sending SMS to {phone_number}: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=2)
def send_bulk_notifications(
    self,
    user_ids: List[int],
    notification_type: str,
    subject: str,
    template: str,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Send notifications to multiple users.
    
    Args:
        user_ids: List of user IDs to notify
        notification_type: Type of notification (email/sms)
        subject: Notification subject
        template: Email template name
        context: Template context
        
    Returns:
        Dict with bulk send statistics
    """
    try:
        context = context or {}
        successful = 0
        failed = 0
        
        from app import db
        from app.models import User
        
        users = User.query.filter(User.id.in_(user_ids)).all()
        
        for user in users:
            try:
                if notification_type == 'email':
                    send_email.delay(
                        user.email,
                        subject,
                        template,
                        {**context, 'user': user.to_dict()}
                    )
                    successful += 1
                elif notification_type == 'sms' and user.phone:
                    send_sms.delay(
                        user.phone,
                        subject
                    )
                    successful += 1
            except Exception as e:
                logger.error(f"Error queuing notification for user {user.id}: {e}")
                failed += 1
        
        logger.info(f"Bulk notifications queued: {successful} successful, {failed} failed")
        return {"successful": successful, "failed": failed}
        
    except Exception as exc:
        logger.error(f"Error in bulk notifications: {exc}")
        raise self.retry(exc=exc)


def _render_email_template(template_name: str, context: Dict[str, Any]) -> str:
    """
    Render email template with context.
    
    Args:
        template_name: Name of the template file
        context: Context variables for rendering
        
    Returns:
        Rendered HTML content
    """
    try:
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('app/templates/emails'))
        template = env.get_template(f"{template_name}.html")
        return template.render(**context)
    except Exception as e:
        logger.error(f"Error rendering email template {template_name}: {e}")
        return "<p>Email template rendering failed.</p>"
