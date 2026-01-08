"""Real-time notification service using WebSockets."""
import json
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import session
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NotificationService:
    """Handles real-time notifications via WebSocket."""
    
    def __init__(self, socketio):
        """Initialize notification service."""
        self.socketio = socketio
        self.user_sessions = {}  # userid -> list of sessionids
    
    def register_user(self, userid: int, sessionid: str):
        """Register user session."""
        if userid not in self.user_sessions:
            self.user_sessions[userid] = []
        self.user_sessions[userid].append(sessionid)
        logger.info(f"User {userid} registered session {sessionid}")
    
    def unregister_user(self, userid: int, sessionid: str):
        """Unregister user session."""
        if userid in self.user_sessions:
            self.user_sessions[userid].remove(sessionid)
            if not self.user_sessions[userid]:
                del self.user_sessions[userid]
        logger.info(f"User {userid} unregistered session {sessionid}")
    
    def notify_user(self, userid: int, notification: dict) -> bool:
        """Send notification to user across all sessions."""
        if userid not in self.user_sessions:
            logger.warning(f"User {userid} has no active sessions")
            return False
        
        notification["timestamp"] = datetime.utcnow().isoformat()
        for sessionid in self.user_sessions[userid]:
            self.socketio.emit("notification", notification, room=sessionid)
        return True
    
    def notify_match(self, userid: int, matchid: int, match_data: dict):
        """Notify user of new match."""
        notification = {
            "type": "new_match",
            "matchid": matchid,
            "match_data": match_data,
            "message": f"New match found with score {match_data.get('score', 0):.1f}"
        }
        return self.notify_user(userid, notification)
    
    def notify_message(self, userid: int, message: str, data: dict = None):
        """Notify user of new message."""
        notification = {
            "type": "message",
            "message": message,
            "data": data or {}
        }
        return self.notify_user(userid, notification)
    
    def notify_application(self, userid: int, application_data: dict):
        """Notify user of new application."""
        notification = {
            "type": "application",
            "application_data": application_data,
            "message": "New application received"
        }
        return self.notify_user(userid, notification)
    
    def notify_broadcast(self, notification: dict):
        """Broadcast notification to all connected users."""
        notification["timestamp"] = datetime.utcnow().isoformat()
        self.socketio.emit("notification", notification)
        logger.info(f"Broadcast notification: {notification['type']}")

def init_websocket(app, socketio):
    """Initialize WebSocket handlers."""
    notification_service = NotificationService(socketio)
    
    @socketio.on("connect")
    def handle_connect():
        logger.info(f"Client connected: {session.get('id')}")
        emit("connect", {"data": "Connected"})
    
    @socketio.on("disconnect")
    def handle_disconnect():
        logger.info(f"Client disconnected: {session.get('id')}")
    
    @socketio.on("register")
    def handle_register(data):
        userid = data.get("userid")
        sessionid = session.get("id")
        notification_service.register_user(userid, sessionid)
        emit("registered", {"userid": userid})
    
    @socketio.on("subscribe_matches")
    def handle_subscribe_matches(data):
        vacancyid = data.get("vacancyid")
        room = f"vacancy_{vacancyid}"
        join_room(room)
        emit("subscribed", {"vacancyid": vacancyid})
    
    @socketio.on("unsubscribe_matches")
    def handle_unsubscribe_matches(data):
        vacancyid = data.get("vacancyid")
        room = f"vacancy_{vacancyid}"
        leave_room(room)
        emit("unsubscribed", {"vacancyid": vacancyid})
    
    return notification_service
