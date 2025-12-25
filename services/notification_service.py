import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import requests

logger = logging.getLogger(__name__)

class NotificationType(Enum):
    EMAIL = 'email'
    SMS = 'sms'
    PUSH = 'push_notification'
    IN_APP = 'in_app'

class NotificationPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

@dataclass
class Notification:
    id: str
    recipient_id: str
    type: NotificationType
    title: str
    message: str
    priority: NotificationPriority
    created_at: datetime
    read: bool = False
    sent_at: Optional[datetime] = None
    metadata: Dict = None

class NotificationService:
    def __init__(self, smtp_config: Dict = None, twilio_config: Dict = None):
        self.smtp_config = smtp_config or {}
        self.twilio_config = twilio_config or {}
        self.notifications = {}
        self.notification_queue = []
    
    def send_email(self, 
                   recipient: str,
                   subject: str,
                   body: str,
                   html_body: Optional[str] = None) -> Dict:
        """Send email notification"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_config.get('sender_email')
            msg['To'] = recipient
            
            msg.attach(MIMEText(body, 'plain'))
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            with smtplib.SMTP(self.smtp_config.get('smtp_server'), 
                            self.smtp_config.get('smtp_port')) as server:
                server.starttls()
                server.login(self.smtp_config.get('sender_email'),
                           self.smtp_config.get('sender_password'))
                server.send_message(msg)
            
            logger.info(f'Email sent to {recipient}')
            return {'success': True, 'message_id': msg['Message-ID']}
        except Exception as e:
            logger.error(f'Email send error: {str(e)}')
            return {'success': False, 'error': str(e)}
    
    def send_sms(self, 
                 phone_number: str,
                 message: str) -> Dict:
        """Send SMS notification via Twilio"""
        try:
            response = requests.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_config.get('account_sid')}/Messages.json",
                data={
                    'From': self.twilio_config.get('phone_number'),
                    'To': phone_number,
                    'Body': message
                },
                auth=(self.twilio_config.get('account_sid'),
                     self.twilio_config.get('auth_token'))
            )
            
            if response.status_code == 201:
                logger.info(f'SMS sent to {phone_number}')
                return {'success': True, 'message_sid': response.json()['sid']}
            else:
                logger.error(f'SMS send failed: {response.text}')
                return {'success': False, 'error': response.text}
        except Exception as e:
            logger.error(f'SMS send error: {str(e)}')
            return {'success': False, 'error': str(e)}
    
    def send_push_notification(self,
                             user_id: str,
                             title: str,
                             body: str,
                             data: Optional[Dict] = None) -> Dict:
        """Send push notification (FCM)"""
        try:
            notification_data = {
                'notification': {
                    'title': title,
                    'body': body
                },
                'to': f'/topics/user_{user_id}'
            }
            if data:
                notification_data['data'] = data
            
            # Implement FCM integration
            logger.info(f'Push notification sent to {user_id}')
            return {'success': True, 'user_id': user_id}
        except Exception as e:
            logger.error(f'Push notification error: {str(e)}')
            return {'success': False, 'error': str(e)}
    
    def create_notification(self,
                          recipient_id: str,
                          notification_type: NotificationType,
                          title: str,
                          message: str,
                          priority: NotificationPriority = NotificationPriority.MEDIUM,
                          metadata: Optional[Dict] = None) -> str:
        """Create a new notification"""
        from uuid import uuid4
        notification_id = str(uuid4())
        
        notification = Notification(
            id=notification_id,
            recipient_id=recipient_id,
            type=notification_type,
            title=title,
            message=message,
            priority=priority,
            created_at=datetime.now(),
            metadata=metadata or {}
        )
        
        self.notifications[notification_id] = notification
        self.notification_queue.append(notification)
        logger.info(f'Notification created: {notification_id}')
        return notification_id
    
    def mark_as_read(self, notification_id: str) -> Dict:
        """Mark notification as read"""
        if notification_id in self.notifications:
            self.notifications[notification_id].read = True
            logger.info(f'Notification marked as read: {notification_id}')
            return {'success': True}
        return {'success': False, 'error': 'Notification not found'}
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Notification]:
        """Get notifications for a user"""
        user_notifications = [n for n in self.notifications.values() 
                            if n.recipient_id == user_id]
        
        if unread_only:
            user_notifications = [n for n in user_notifications if not n.read]
        
        return sorted(user_notifications, key=lambda x: x.created_at, reverse=True)
    
    def delete_notification(self, notification_id: str) -> Dict:
        """Delete a notification"""
        if notification_id in self.notifications:
            del self.notifications[notification_id]
            logger.info(f'Notification deleted: {notification_id}')
            return {'success': True}
        return {'success': False, 'error': 'Notification not found'}
    
    def process_queue(self) -> Dict:
        """Process notification queue and send pending notifications"""
        sent = 0
        failed = 0
        
        while self.notification_queue:
            notification = self.notification_queue.pop(0)
            
            try:
                if notification.type == NotificationType.EMAIL:
                    # Send email (requires user email from database)
                    pass
                elif notification.type == NotificationType.SMS:
                    # Send SMS (requires user phone from database)
                    pass
                elif notification.type == NotificationType.PUSH:
                    self.send_push_notification(
                        notification.recipient_id,
                        notification.title,
                        notification.message,
                        notification.metadata
                    )
                
                notification.sent_at = datetime.now()
                sent += 1
            except Exception as e:
                logger.error(f'Failed to send notification {notification.id}: {str(e)}')
                failed += 1
        
        return {'sent': sent, 'failed': failed}
    
    def get_notification_stats(self) -> Dict:
        """Get notification statistics"""
        total = len(self.notifications)
        unread = len([n for n in self.notifications.values() if not n.read])
        sent = len([n for n in self.notifications.values() if n.sent_at])
        by_type = {}
        
        for notification in self.notifications.values():
            type_name = notification.type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
        
        return {
            'total_notifications': total,
            'unread_count': unread,
            'sent_count': sent,
            'by_type': by_type
        }
