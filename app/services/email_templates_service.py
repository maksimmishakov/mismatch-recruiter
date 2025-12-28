email_templates_service.py"""Email Templates Service

Manages HTML/plain text email templates for:
- Job match notifications
- Placement confirmations
- Recruitment summaries
- Weekly reports
"""
import logging
from typing import Dict, Optional, List
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class EmailTemplate(Enum):
    """Available email templates"""
    JOB_MATCH = "job_match"
    PLACEMENT_SUBMITTED = "placement_submitted"
    PLACEMENT_UPDATE = "placement_update"
    WEEKLY_SUMMARY = "weekly_summary"
    DAILY_DIGEST = "daily_digest"
    ERROR_ALERT = "error_alert"


class EmailTemplatesService:
    """Service for managing email templates"""
    
    def __init__(self):
        """Initialize templates service"""
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """Load all email templates
        
        Returns:
            Dict with template definitions
        """
        return {
            EmailTemplate.JOB_MATCH.value: {
                "subject": "New Job Match: {job_title}",
                "html": self._get_job_match_html(),
                "text": self._get_job_match_text()
            },
            EmailTemplate.PLACEMENT_SUBMITTED.value: {
                "subject": "Placement Submitted: {candidate_name} -> {job_title}",
                "html": self._get_placement_submitted_html(),
                "text": self._get_placement_submitted_text()
            },
            EmailTemplate.PLACEMENT_UPDATE.value: {
                "subject": "Placement Update: {status}",
                "html": self._get_placement_update_html(),
                "text": self._get_placement_update_text()
            },
            EmailTemplate.WEEKLY_SUMMARY.value: {
                "subject": "Weekly Recruitment Summary",
                "html": self._get_weekly_summary_html(),
                "text": self._get_weekly_summary_text()
            },
            EmailTemplate.DAILY_DIGEST.value: {
                "subject": "Daily Recruitment Digest",
                "html": self._get_daily_digest_html(),
                "text": self._get_daily_digest_text()
            },
            EmailTemplate.ERROR_ALERT.value: {
                "subject": "Alert: {error_type}",
                "html": self._get_error_alert_html(),
                "text": self._get_error_alert_text()
            }
        }
    
    def _get_job_match_html(self) -> str:
        """Get job match HTML template"""
        return """<html><body>
<h2>New Job Match Found!</h2>
<p>Candidate: <strong>{candidate_name}</strong></p>
<p>Position: <strong>{job_title}</strong> at {company}</p>
<p>Match Score: <strong>{match_score}%</strong></p>
<p><a href="{view_url}">View Details</a></p>
</body></html>"""
    
    def _get_job_match_text(self) -> str:
        return """New Job Match Found!
Candidate: {candidate_name}
Position: {job_title} at {company}
Match Score: {match_score}%
View Details: {view_url}"""
    
    def _get_placement_submitted_html(self) -> str:
        """Get placement submitted HTML template"""
        return """<html><body>
<h2>Placement Submitted</h2>
<p>Candidate: <strong>{candidate_name}</strong></p>
<p>Position: <strong>{job_title}</strong></p>
<p>Company: {company}</p>
<p>Submitted: {submitted_date}</p>
<p><a href="{track_url}">Track Status</a></p>
</body></html>"""
    
    def _get_placement_submitted_text(self) -> str:
        return """Placement Submitted
Candidate: {candidate_name}
Position: {job_title}
Company: {company}
Submitted: {submitted_date}
Track Status: {track_url}"""
    
    def _get_placement_update_html(self) -> str:
        """Get placement update HTML template"""
        return """<html><body>
<h2>Placement Status Update</h2>
<p>Status: <strong>{status}</strong></p>
<p>Candidate: {candidate_name}</p>
<p>Position: {job_title}</p>
<p>Updated: {updated_date}</p>
<p>{message}</p>
</body></html>"""
    
    def _get_placement_update_text(self) -> str:
        return """Placement Status Update
Status: {status}
Candidate: {candidate_name}
Position: {job_title}
Updated: {updated_date}
{message}"""
    
    def _get_weekly_summary_html(self) -> str:
        """Get weekly summary HTML template"""
        return """<html><body>
<h2>Weekly Recruitment Summary</h2>
<p>Week of {week_start} to {week_end}</p>
<ul>
<li>New Matches: {new_matches}</li>
<li>Placements Submitted: {placements_submitted}</li>
<li>Interviews Scheduled: {interviews}</li>
<li>Offers Made: {offers}</li>
</ul>
</body></html>"""
    
    def _get_weekly_summary_text(self) -> str:
        return """Weekly Recruitment Summary
Week of {week_start} to {week_end}
New Matches: {new_matches}
Placements Submitted: {placements_submitted}
Interviews Scheduled: {interviews}
Offers Made: {offers}"""
    
    def _get_daily_digest_html(self) -> str:
        """Get daily digest HTML template"""
        return """<html><body>
<h2>Daily Recruitment Digest - {date}</h2>
<p>Active Placements: {active_placements}</p>
<p>Today's Matches: {today_matches}</p>
<p>Pending Actions: {pending_actions}</p>
</body></html>"""
    
    def _get_daily_digest_text(self) -> str:
        return """Daily Recruitment Digest - {date}
Active Placements: {active_placements}
Today's Matches: {today_matches}
Pending Actions: {pending_actions}"""
    
    def _get_error_alert_html(self) -> str:
        """Get error alert HTML template"""
        return """<html><body>
<h2 style="color:red;">Error Alert</h2>
<p>Error Type: <strong>{error_type}</strong></p>
<p>Message: {error_message}</p>
<p>Time: {error_time}</p>
</body></html>"""
    
    def _get_error_alert_text(self) -> str:
        return """Error Alert
Error Type: {error_type}
Message: {error_message}
Time: {error_time}"""
    
    def get_template(self, template_type: str) -> Optional[Dict[str, str]]:
        """Get specific template
        
        Args:
            template_type: Template identifier
            
        Returns:
            Template dict with subject, html, text keys
        """
        return self.templates.get(template_type)
    
    def render_template(self, 
                       template_type: str,
                       context: Dict[str, str]) -> Optional[Dict[str, str]]:
        """Render template with context variables
        
        Args:
            template_type: Template identifier
            context: Variables dict for template
            
        Returns:
            Rendered template with subject, html, text
        """
        template = self.get_template(template_type)
        if not template:
            logger.error(f"Template not found: {template_type}")
            return None
        
        try:
            return {
                "subject": template["subject"].format(**context),
                "html": template["html"].format(**context),
                "text": template["text"].format(**context)
            }
        except KeyError as e:
            logger.error(f"Missing template variable: {e}")
            return None
    
    def list_templates(self) -> List[str]:
        """List all available templates
        
        Returns:
            List of template identifiers
        """
        return list(self.templates.keys())


# Singleton instance
_email_service: Optional[EmailTemplatesService] = None


def get_email_templates_service() -> EmailTemplatesService:
    """Get or create singleton email templates service
    
    Returns:
        EmailTemplatesService instance
    """
    global _email_service
    if _email_service is None:
        _email_service = EmailTemplatesService()
    return _email_service
