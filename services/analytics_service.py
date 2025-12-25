import json
from datetime import datetime
from collections import defaultdict

class AnalyticsService:
    """Track user events and generate analytics"""
    
    def __init__(self):
        self.events = []
        self.event_counts = defaultdict(int)
    
    def track_event(self, event_name, user_id=None, metadata=None):
        """Track an event"""
        event = {
            'event': event_name,
            'user_id': user_id or 'anonymous',
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.events.append(event)
        self.event_counts[event_name] += 1
        
        return event
    
    def get_event_count(self, event_name):
        """Get count for specific event"""
        return self.event_counts.get(event_name, 0)
    
    def get_events(self, event_name=None, limit=100):
        """Get events, optionally filtered by name"""
        if event_name:
            events = [e for e in self.events if e['event'] == event_name]
        else:
            events = self.events
        
        return events[-limit:]
    
    def get_analytics_summary(self):
        """Get summary of all tracked events"""
        return {
            'total_events': len(self.events),
            'event_types': dict(self.event_counts),
            'top_events': sorted(self.event_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            'timestamp': datetime.now().isoformat()
        }
    
    def clear_events(self):
        """Clear event history"""
        self.events = []
        self.event_counts.clear()

analytics_service = AnalyticsService()
