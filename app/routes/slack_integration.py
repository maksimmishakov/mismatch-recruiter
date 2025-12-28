import os
import logging
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.slack_service import SlackService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/slack", tags=["slack"])

# Initialize Slack service with webhook URL from environment
slack_webhook = os.getenv("SLACK_WEBHOOK_URL", "")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN", "")
slack_service = SlackService(webhook_url=slack_webhook, bot_token=slack_bot_token)


class SlackConfig(BaseModel):
    """Slack configuration model"""
    webhook_url: str
    bot_token: Optional[str] = None
    channel: str = "#mismatch-alerts"


class TestMessage(BaseModel):
    """Test message model"""
    channel: str
    message: Optional[str] = None


class SubscriptionRequest(BaseModel):
    """Subscription request model"""
    event_type: str  # match, daily_summary, report, error
    channel: str
    enabled: bool = True


@router.post("/config")
async def configure_slack(config: SlackConfig):
    """Configure Slack webhook and bot token
    
    Args:
        config: Slack configuration with webhook_url, bot_token, and channel
        
    Returns:
        Configuration status and confirmation
    """
    try:
        # Update global Slack service with new configuration
        global slack_service
        slack_service = SlackService(
            webhook_url=config.webhook_url,
            bot_token=config.bot_token
        )
        
        # Store configuration (in production, save to database)
        logger.info(f"Slack configured for channel: {config.channel}")
        
        return {
            "status": "success",
            "message": f"Slack integration configured for {config.channel}",
            "webhook_configured": bool(config.webhook_url),
            "bot_token_configured": bool(config.bot_token)
        }
    except Exception as e:
        logger.error(f"Failed to configure Slack: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Configuration failed: {str(e)}"
        )


@router.post("/test")
async def test_slack_connection(message: TestMessage):
    """Test Slack connection
    
    Args:
        message: Test message configuration with channel and optional message text
        
    Returns:
        Test result with success/failure status
    """
    try:
        if not slack_service.webhook_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slack webhook URL not configured"
            )
        
        # Send test message
        test_text = message.message or "This is a test message from MisMatch. If you see this, the integration is working! ✅"
        result = slack_service.send_notification(
            channel=message.channel,
            title="Test Message",
            text=test_text,
            color="#00aa00"
        )
        
        if result:
            logger.info(f"Test message sent to {message.channel}")
            return {
                "status": "success",
                "message": f"Test message sent to {message.channel}"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send test message"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Test failed: {str(e)}"
        )


@router.post("/subscribe")
async def subscribe_to_events(subscription: SubscriptionRequest):
    """Subscribe to Slack notifications for specific events
    
    Args:
        subscription: Subscription request with event_type, channel, and enabled status
        
    Returns:
        Subscription confirmation
    """
    try:
        # Validate event type
        valid_events = ["match", "daily_summary", "report", "error", "perfect_match"]
        if subscription.event_type not in valid_events:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid event type. Must be one of: {', '.join(valid_events)}"
            )
        
        # Store subscription (in production, save to database)
        logger.info(
            f"User subscribed to {subscription.event_type} events "
            f"in {subscription.channel} (enabled={subscription.enabled})"
        )
        
        return {
            "status": "success",
            "message": f"Subscribed to {subscription.event_type} events",
            "event_type": subscription.event_type,
            "channel": subscription.channel,
            "enabled": subscription.enabled
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Subscription failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Subscription failed: {str(e)}"
        )


@router.get("/status")
async def get_slack_status():
    """Get Slack integration status
    
    Returns:
        Status of Slack integration
    """
    try:
        webhook_configured = bool(slack_service.webhook_url)
        
        return {
            "status": "connected" if webhook_configured else "not_configured",
            "webhook_configured": webhook_configured,
            "bot_token_configured": bool(slack_service.bot_token),
            "message": "Slack integration is ready" if webhook_configured else "Please configure Slack webhook"
        }
    except Exception as e:
        logger.error(f"Failed to get status: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


@router.post("/notify/match")
async def notify_match(job_title: str, candidate_name: str, score: float, channel: str = "#mismatch-alerts"):
    """Send match notification to Slack
    
    Args:
        job_title: Job position title
        candidate_name: Candidate name
        score: Match score (0-1)
        channel: Slack channel
        
    Returns:
        Notification result
    """
    try:
        result = slack_service.send_match_alert(
            channel=channel,
            job_title=job_title,
            candidate_name=candidate_name,
            score=score,
            dashboard_link="https://localhost:8000/dashboard"
        )
        
        if result:
            return {
                "status": "success",
                "message": f"Match notification sent: {candidate_name} → {job_title}"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send match notification"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to send match notification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send notification: {str(e)}"
        )
