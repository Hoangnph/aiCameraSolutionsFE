import asyncio
import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import redis.asyncio as redis
import httpx
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertType(Enum):
    CAMERA_OFFLINE = "camera_offline"
    CAMERA_ERROR = "camera_error"
    HIGH_COUNT = "high_count"
    SYSTEM_ERROR = "system_error"
    SECURITY_BREACH = "security_breach"
    PERFORMANCE_ISSUE = "performance_issue"
    DATABASE_ERROR = "database_error"
    REDIS_ERROR = "redis_error"

@dataclass
class Alert:
    id: str
    type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    camera_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    acknowledged: bool = False
    resolved: bool = False

class AlertService:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.alert_history: List[Alert] = []
        self.alert_rules: Dict[str, Dict] = {}
        self.notification_channels: Dict[str, Any] = {}
        self.rate_limits: Dict[str, datetime] = {}
        
        # Load default alert rules
        self._load_default_rules()
    
    def _load_default_rules(self):
        """Load default alert rules"""
        self.alert_rules = {
            AlertType.CAMERA_OFFLINE.value: {
                'threshold': 300,  # 5 minutes
                'rate_limit': 300,  # 5 minutes between alerts
                'severity': AlertSeverity.WARNING,
                'channels': ['email', 'websocket', 'database']
            },
            AlertType.CAMERA_ERROR.value: {
                'threshold': 1,
                'rate_limit': 60,  # 1 minute between alerts
                'severity': AlertSeverity.ERROR,
                'channels': ['email', 'websocket', 'database']
            },
            AlertType.HIGH_COUNT.value: {
                'threshold': 100,  # 100 people
                'rate_limit': 300,  # 5 minutes between alerts
                'severity': AlertSeverity.WARNING,
                'channels': ['websocket', 'database']
            },
            AlertType.SYSTEM_ERROR.value: {
                'threshold': 1,
                'rate_limit': 60,
                'severity': AlertSeverity.CRITICAL,
                'channels': ['email', 'websocket', 'database', 'sms']
            },
            AlertType.SECURITY_BREACH.value: {
                'threshold': 1,
                'rate_limit': 0,  # No rate limit for security alerts
                'severity': AlertSeverity.CRITICAL,
                'channels': ['email', 'websocket', 'database', 'sms']
            },
            AlertType.PERFORMANCE_ISSUE.value: {
                'threshold': 2,  # 2 seconds response time
                'rate_limit': 300,
                'severity': AlertSeverity.WARNING,
                'channels': ['websocket', 'database']
            }
        }
    
    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
            await self.redis_client.ping()
            logger.info("Alert service connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
    
    async def create_alert(self, alert_type: AlertType, title: str, message: str, 
                          severity: Optional[AlertSeverity] = None, 
                          camera_id: Optional[str] = None,
                          metadata: Optional[Dict[str, Any]] = None) -> Alert:
        """Create and send a new alert"""
        
        # Check rate limiting
        if not await self._check_rate_limit(alert_type.value):
            logger.info(f"Alert rate limited for type: {alert_type.value}")
            return None
        
        # Get severity from rules if not provided
        if not severity:
            severity = self.alert_rules.get(alert_type.value, {}).get('severity', AlertSeverity.INFO)
        
        # Create alert
        alert = Alert(
            id=f"{alert_type.value}_{datetime.utcnow().timestamp()}",
            type=alert_type,
            severity=severity,
            title=title,
            message=message,
            camera_id=camera_id,
            metadata=metadata or {},
            timestamp=datetime.utcnow()
        )
        
        # Store alert
        await self._store_alert(alert)
        
        # Send notifications
        await self._send_notifications(alert)
        
        # Update rate limit
        self._update_rate_limit(alert_type.value)
        
        logger.info(f"Alert created: {alert.id} - {alert.title}")
        return alert
    
    async def _check_rate_limit(self, alert_type: str) -> bool:
        """Check if alert is within rate limit"""
        rule = self.alert_rules.get(alert_type, {})
        rate_limit = rule.get('rate_limit', 0)
        
        if rate_limit == 0:
            return True
        
        last_alert = self.rate_limits.get(alert_type)
        if not last_alert:
            return True
        
        time_since_last = datetime.utcnow() - last_alert
        return time_since_last.total_seconds() >= rate_limit
    
    def _update_rate_limit(self, alert_type: str):
        """Update rate limit timestamp"""
        self.rate_limits[alert_type] = datetime.utcnow()
    
    async def _store_alert(self, alert: Alert):
        """Store alert in Redis and local history"""
        # Store in Redis
        if self.redis_client:
            alert_data = {
                'id': alert.id,
                'type': alert.type.value,
                'severity': alert.severity.value,
                'title': alert.title,
                'message': alert.message,
                'camera_id': alert.camera_id,
                'metadata': json.dumps(alert.metadata),
                'timestamp': alert.timestamp.isoformat(),
                'acknowledged': alert.acknowledged,
                'resolved': alert.resolved
            }
            
            # Store in Redis with TTL (30 days)
            await self.redis_client.hset(f"alert:{alert.id}", mapping=alert_data)
            await self.redis_client.expire(f"alert:{alert.id}", 30 * 24 * 3600)
            
            # Add to alert list
            await self.redis_client.lpush("alerts:recent", alert.id)
            await self.redis_client.ltrim("alerts:recent", 0, 999)  # Keep last 1000 alerts
        
        # Store in local history
        self.alert_history.append(alert)
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]
    
    async def _send_notifications(self, alert: Alert):
        """Send notifications through configured channels"""
        rule = self.alert_rules.get(alert.type.value, {})
        channels = rule.get('channels', [])
        
        for channel in channels:
            try:
                if channel == 'email':
                    await self._send_email_alert(alert)
                elif channel == 'websocket':
                    await self._send_websocket_alert(alert)
                elif channel == 'database':
                    await self._store_database_alert(alert)
                elif channel == 'sms':
                    await self._send_sms_alert(alert)
            except Exception as e:
                logger.error(f"Failed to send {channel} notification: {e}")
    
    async def _send_email_alert(self, alert: Alert):
        """Send email alert"""
        try:
            # Email configuration from environment
            smtp_host = "smtp.gmail.com"
            smtp_port = 587
            smtp_user = "your_email@gmail.com"
            smtp_password = "your_app_password"
            email_from = "noreply@your-domain.com"
            email_to = "admin@your-domain.com"
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = email_to
            msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.title}"
            
            body = f"""
            Alert Details:
            --------------
            Type: {alert.type.value}
            Severity: {alert.severity.value}
            Title: {alert.title}
            Message: {alert.message}
            Camera ID: {alert.camera_id or 'N/A'}
            Timestamp: {alert.timestamp}
            
            Metadata: {json.dumps(alert.metadata, indent=2)}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email alert sent: {alert.id}")
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
    
    async def _send_websocket_alert(self, alert: Alert):
        """Send WebSocket alert"""
        try:
            alert_data = {
                'type': 'alert',
                'alert_type': alert.type.value,
                'severity': alert.severity.value,
                'title': alert.title,
                'message': alert.message,
                'camera_id': alert.camera_id,
                'metadata': alert.metadata,
                'timestamp': alert.timestamp.isoformat()
            }
            
            # Publish to Redis for WebSocket service
            if self.redis_client:
                await self.redis_client.publish('alerts', json.dumps(alert_data))
            
            logger.info(f"WebSocket alert sent: {alert.id}")
            
        except Exception as e:
            logger.error(f"Failed to send WebSocket alert: {e}")
    
    async def _store_database_alert(self, alert: Alert):
        """Store alert in database"""
        try:
            # This would typically store in PostgreSQL
            # For now, we'll just log it
            logger.info(f"Database alert stored: {alert.id}")
            
        except Exception as e:
            logger.error(f"Failed to store database alert: {e}")
    
    async def _send_sms_alert(self, alert: Alert):
        """Send SMS alert (placeholder)"""
        try:
            # This would integrate with SMS service like Twilio
            logger.info(f"SMS alert sent: {alert.id}")
            
        except Exception as e:
            logger.error(f"Failed to send SMS alert: {e}")
    
    async def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        try:
            if self.redis_client:
                await self.redis_client.hset(f"alert:{alert_id}", "acknowledged", True)
            
            # Update local history
            for alert in self.alert_history:
                if alert.id == alert_id:
                    alert.acknowledged = True
                    break
            
            logger.info(f"Alert acknowledged: {alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to acknowledge alert: {e}")
            return False
    
    async def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert"""
        try:
            if self.redis_client:
                await self.redis_client.hset(f"alert:{alert_id}", "resolved", True)
            
            # Update local history
            for alert in self.alert_history:
                if alert.id == alert_id:
                    alert.resolved = True
                    break
            
            logger.info(f"Alert resolved: {alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to resolve alert: {e}")
            return False
    
    async def get_recent_alerts(self, limit: int = 50) -> List[Alert]:
        """Get recent alerts"""
        try:
            if self.redis_client:
                alert_ids = await self.redis_client.lrange("alerts:recent", 0, limit - 1)
                alerts = []
                
                for alert_id in alert_ids:
                    alert_data = await self.redis_client.hgetall(f"alert:{alert_id}")
                    if alert_data:
                        alert = Alert(
                            id=alert_data['id'],
                            type=AlertType(alert_data['type']),
                            severity=AlertSeverity(alert_data['severity']),
                            title=alert_data['title'],
                            message=alert_data['message'],
                            camera_id=alert_data.get('camera_id'),
                            metadata=json.loads(alert_data.get('metadata', '{}')),
                            timestamp=datetime.fromisoformat(alert_data['timestamp']),
                            acknowledged=alert_data.get('acknowledged', 'false') == 'true',
                            resolved=alert_data.get('resolved', 'false') == 'true'
                        )
                        alerts.append(alert)
                
                return alerts
            
            return self.alert_history[-limit:]
            
        except Exception as e:
            logger.error(f"Failed to get recent alerts: {e}")
            return []
    
    async def get_alerts_by_type(self, alert_type: AlertType, limit: int = 50) -> List[Alert]:
        """Get alerts by type"""
        try:
            alerts = []
            for alert in reversed(self.alert_history):
                if alert.type == alert_type:
                    alerts.append(alert)
                    if len(alerts) >= limit:
                        break
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to get alerts by type: {e}")
            return []
    
    async def get_alerts_by_severity(self, severity: AlertSeverity, limit: int = 50) -> List[Alert]:
        """Get alerts by severity"""
        try:
            alerts = []
            for alert in reversed(self.alert_history):
                if alert.severity == severity:
                    alerts.append(alert)
                    if len(alerts) >= limit:
                        break
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to get alerts by severity: {e}")
            return []
    
    async def cleanup_old_alerts(self, days: int = 30):
        """Clean up old alerts"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Clean local history
            self.alert_history = [
                alert for alert in self.alert_history 
                if alert.timestamp > cutoff_date
            ]
            
            logger.info(f"Cleaned up alerts older than {days} days")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old alerts: {e}")

# Global alert service instance
alert_service = AlertService()

# Convenience functions for common alerts
async def alert_camera_offline(camera_id: str, duration_seconds: int):
    """Alert when camera goes offline"""
    await alert_service.create_alert(
        AlertType.CAMERA_OFFLINE,
        f"Camera {camera_id} is offline",
        f"Camera {camera_id} has been offline for {duration_seconds} seconds",
        camera_id=camera_id,
        metadata={'duration_seconds': duration_seconds}
    )

async def alert_camera_error(camera_id: str, error_message: str):
    """Alert when camera encounters an error"""
    await alert_service.create_alert(
        AlertType.CAMERA_ERROR,
        f"Camera {camera_id} error",
        f"Camera {camera_id} encountered an error: {error_message}",
        camera_id=camera_id,
        metadata={'error_message': error_message}
    )

async def alert_high_count(camera_id: str, count: int, threshold: int):
    """Alert when people count exceeds threshold"""
    await alert_service.create_alert(
        AlertType.HIGH_COUNT,
        f"High people count detected",
        f"Camera {camera_id} detected {count} people (threshold: {threshold})",
        camera_id=camera_id,
        metadata={'count': count, 'threshold': threshold}
    )

async def alert_system_error(error_message: str, component: str):
    """Alert for system errors"""
    await alert_service.create_alert(
        AlertType.SYSTEM_ERROR,
        f"System error in {component}",
        f"System error in {component}: {error_message}",
        metadata={'component': component, 'error_message': error_message}
    )

async def alert_security_breach(event_type: str, details: str):
    """Alert for security breaches"""
    await alert_service.create_alert(
        AlertType.SECURITY_BREACH,
        f"Security breach detected",
        f"Security breach: {event_type} - {details}",
        metadata={'event_type': event_type, 'details': details}
    )

async def alert_performance_issue(component: str, metric: str, value: float, threshold: float):
    """Alert for performance issues"""
    await alert_service.create_alert(
        AlertType.PERFORMANCE_ISSUE,
        f"Performance issue in {component}",
        f"{component} {metric} is {value} (threshold: {threshold})",
        metadata={'component': component, 'metric': metric, 'value': value, 'threshold': threshold}
    ) 