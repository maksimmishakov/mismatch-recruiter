import json
import logging
import requests
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Slack message types"""
    NOTIFICATION = "notification"
    ALERT = "alert"
    SUMMARY = "summary"
    REPORT = "report"


class SlackService:
    """Service for sending notifications to Slack"""
    
    def __init__(self, webhook_url: str, bot_token: Optional[str] = None):
        """Initialize Slack service
        
        Args:
            webhook_url: Slack webhook URL for incoming webhooks
            bot_token: Slack bot token (optional, for more advanced operations)
        """
        self.webhook_url = webhook_url
        self.bot_token = bot_token
        self.base_url = "https://slack.com/api"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bot_token}" if bot_token else ""
        }
    
    def send_notification(
        self,
        channel: str,
        title: str,
        text: str,
        fields: Optional[Dict[str, str]] = None,
        color: str = "#36a64f"
    ) -> bool:
        """Send a notification to Slack
        
        Args:
            channel: Slack channel name or ID
            title: Message title
            text: Message text
            fields: Optional dictionary of field names and values
            color: Message color (hex code)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            payload = {
                "channel": channel,
                "attachments": [{
                    "fallback": title,
                    "color": color,
                    "title": title,
                    "text": text,
                    "ts": int(datetime.now().timestamp())
                }]
            }
            
            if fields:
                payload["attachments"][0]["fields"] = [
                    {"title": k, "value": v, "short": True}
                    for k, v in fields.items()
                ]
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Slack notification sent to {channel}")
                return True
            else:
                logger.error(f"Failed to send Slack notification: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Slack notification: {str(e)}")
            return False
    
    def send_match_alert(
        self,
        channel: str,
        job_title: str,
        candidate_name: str,
        score: float,
        match_explanation: str = "",
        dashboard_link: str = ""
    ) -> bool:
        """Send a match alert to Slack
        
        Args:
            channel: Slack channel
            job_title: Job position title
            candidate_name: Candidate name
            score: Match score (0-1)
            match_explanation: Brief explanation of the match
            dashboard_link: Link to view in dashboard
            
        Returns:
            True if successful
        """
        try:
            # Determine color based on score
            if score >= 0.85:
                color = "#00aa00"  # Green - perfect match
                emoji = "🎯"
            elif score >= 0.70:
                color = "#ffaa00"  # Orange - good match
                emoji = "👍"
            else:
                color = "#0066cc"  # Blue - potential match
                emoji = "📋"
            
            fields = {
                "Job Position": job_title,
                "Candidate": candidate_name,
                "Match Score": f"{score * 100:.1f}%",
            }
            
            if match_explanation:
                fields["Explanation"] = match_explanation
            
            payload = {
                "channel": channel,
                "attachments": [{
                    "fallback": f"{emoji} New Match: {candidate_name} for {job_title}",
                    "color": color,
                    "title": f"{emoji} New Match Found!",
                    "fields": [
                        {"title": k, "value": v, "short": True}
                        for k, v in fields.items()
                    ],
                    "actions": [
                        {
                            "type": "button",
                            "text": "View in Dashboard",
                            "url": dashboard_link if dashboard_link else "#"
                        }
                    ] if dashboard_link else [],
                    "ts": int(datetime.now().timestamp())
                }]
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Match alert sent: {candidate_name} → {job_title}")
                return True
            else:
                logger.error(f"Failed to send match alert: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending match alert: {str(e)}")
            return False
    
    def send_daily_summary(
        self,
        channel: str,
        metrics: Dict[str, any]
    ) -> bool:
        """Send daily summary to Slack
        
        Args:
            channel: Slack channel
            metrics: Dictionary with metrics (total_matches, success_rate, etc.)
            
        Returns:
            True if successful
        """
        try:
            payload = {
                "channel": channel,
                "attachments": [{
                    "fallback": "Daily Summary",
                    "color": "#4169e1",
                    "title": "📊 Daily Summary",
                    "fields": [
                        {"title": "Total Matches", "value": str(metrics.get('total_matches', 0)), "short": True},
                        {"title": "Success Rate", "value": f"{metrics.get('success_rate', 0):.1f}%", "short": True},
                        {"title": "Top Job", "value": metrics.get('top_job', 'N/A'), "short": True},
                        {"title": "Top Candidate", "value": metrics.get('top_candidate', 'N/A'), "short": True},
                        {"title": "Average Match Score", "value": f"{metrics.get('avg_score', 0):.2f}", "short": True},
                    ],
                    "footer": "MisMatch Platform",
                    "ts": int(datetime.now().timestamp())
                }]
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info("Daily summary sent to Slack")
                return True
            else:
                logger.error(f"Failed to send daily summary: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending daily summary: {str(e)}")
            return False
    
    def send_report(
        self,
        channel: str,
        report_type: str,
        filename: str,
        download_link: str
    ) -> bool:
        """Send report notification to Slack
        
        Args:
            channel: Slack channel
            report_type: Type of report (daily, weekly, monthly)
            filename: Report filename
            download_link: Link to download report
            
        Returns:
            True if successful
        """
        try:
            payload = {
                "channel": channel,
                "attachments": [{
                    "fallback": f"{report_type.capitalize()} Report Ready",
                    "color": "#9c27b0",
                    "title": f"📄 {report_type.capitalize()} Report Ready",
                    "text": f"Report: {filename}",
                    "fields": [
                        {"title": "Report Type", "value": report_type, "short": True},
                        {"title": "Generated", "value": datetime.now().strftime('%Y-%m-%d %H:%M'), "short": True},
                    ],
                    "actions": [
                        {
                            "type": "button",
                            "text": "Download Report",
                            "url": download_link
                        }
                    ],
                    "footer": "MisMatch Platform",
                    "ts": int(datetime.now().timestamp())
                }]
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Report notification sent: {filename}")
                return True
            else:
                logger.error(f"Failed to send report notification: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending report notification: {str(e)}")
            return False
    
    def test_connection(self, channel: str) -> bool:
        """Test Slack connection
        
        Args:
            channel: Slack channel to test
            
        Returns:
            True if connection successful
        """
        return self.send_notification(
            channel=channel,
            title="Test Connection",
            text="This is a test message from MisMatch. If you see this, the integration is working! ✅",
            color="#00aa00"
        )
