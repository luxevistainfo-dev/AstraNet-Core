# ai/alert_system.py

import json
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import threading
import time

class AIAlertSystem:
    def __init__(self, config_file="alert_config.json"):
        self.config_file = config_file
        self.alerts = []
        self.alert_history = []
        self.config = self.load_config()
        self.running = False
        self.alert_thread = None
        
        print(f"[ALERT] Alert system initialized")
        print(f"[ALERT] Alert channels: {', '.join(self.config['alert_channels'])}")
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "alert_channels": ["console", "log"],
            "email_config": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipients": []
            },
            "telegram_config": {
                "enabled": False,
                "bot_token": "",
                "chat_id": ""
            },
            "alert_thresholds": {
                "high_risk_tx": 0.8,
                "suspicious_pattern": 0.7,
                "node_down": 300,  # seconds
                "high_cpu": 90,    # percentage
                "high_memory": 90, # percentage
                "low_disk": 10     # percentage free
            },
            "cooldown_periods": {
                "same_alert": 300,  # 5 minutes
                "same_node": 60     # 1 minute
            }
        }
        
        try:
            with open(self.config_file, 'r') as f:
                loaded = json.load(f)
                # Update defaults with loaded values
                for key in loaded:
                    if key in default_config:
                        if isinstance(default_config[key], dict) and isinstance(loaded[key], dict):
                            default_config[key].update(loaded[key])
                        else:
                            default_config[key] = loaded[key]
        except FileNotFoundError:
            print(f"[ALERT] Config file not found, using defaults")
        
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def check_transaction_risk(self, transaction, ai_score):
        """Check if transaction triggers risk alert"""
        alerts = []
        
        if ai_score > self.config["alert_thresholds"]["high_risk_tx"]:
            alerts.append({
                "type": "HIGH_RISK_TRANSACTION",
                "severity": "CRITICAL",
                "message": f"High risk transaction detected: {getattr(transaction, 'tx_id', 'unknown')}",
                "score": ai_score,
                "threshold": self.config["alert_thresholds"]["high_risk_tx"],
                "data": {
                    "sender": getattr(transaction, 'sender', 'unknown'),
                    "receiver": getattr(transaction, 'receiver', 'unknown'),
                    "amount": getattr(transaction, 'amount', 0)
                }
            })
        
        # Check for suspicious patterns
        if hasattr(transaction, 'amount') and transaction.amount <= 0:
            alerts.append({
                "type": "INVALID_AMOUNT",
                "severity": "MEDIUM",
                "message": f"Transaction with invalid amount: {transaction.amount}",
                "data": {
                    "tx_id": getattr(transaction, 'tx_id', 'unknown')
                }
            })
        
        return alerts
    
    def check_node_health(self, node_metrics):
        """Check if node health triggers alert"""
        alerts = []
        
        cpu = node_metrics.get('cpu_percent', 0)
        memory = node_metrics.get('memory_percent', 0)
        disk_free = node_metrics.get('disk_free_percent', 100)
        
        if cpu > self.config["alert_thresholds"]["high_cpu"]:
            alerts.append({
                "type": "HIGH_CPU_USAGE",
                "severity": "HIGH",
                "message": f"High CPU usage: {cpu}%",
                "value": cpu,
                "threshold": self.config["alert_thresholds"]["high_cpu"]
            })
        
        if memory > self.config["alert_thresholds"]["high_memory"]:
            alerts.append({
                "type": "HIGH_MEMORY_USAGE",
                "severity": "HIGH",
                "message": f"High memory usage: {memory}%",
                "value": memory,
                "threshold": self.config["alert_thresholds"]["high_memory"]
            })
        
        if disk_free < self.config["alert_thresholds"]["low_disk"]:
            alerts.append({
                "type": "LOW_DISK_SPACE",
                "severity": "HIGH",
                "message": f"Low disk space: {disk_free}% free",
                "value": disk_free,
                "threshold": self.config["alert_thresholds"]["low_disk"]
            })
        
        return alerts
    
    def check_network_anomalies(self, network_metrics):
        """Check for network anomalies"""
        alerts = []
        
        latency = network_metrics.get('avg_latency', 0)
        node_count = network_metrics.get('active_nodes', 0)
        
        if latency > 1000:  # More than 1 second
            alerts.append({
                "type": "HIGH_NETWORK_LATENCY",
                "severity": "MEDIUM",
                "message": f"High network latency: {latency}ms",
                "value": latency
            })
        
        if node_count < 3:  # Less than 3 active nodes
            alerts.append({
                "type": "LOW_NODE_COUNT",
                "severity": "HIGH",
                "message": f"Low node count: {node_count} active nodes",
                "value": node_count
            })
        
        return alerts
    
    def should_alert(self, alert_type, node_id=None):
        """Check if we should send this alert (cooldown)"""
        now = datetime.now()
        cooldown_period = self.config["cooldown_periods"]["same_alert"]
        
        # Check for recent similar alerts
        for alert in reversed(self.alert_history[-20:]):  # Check last 20 alerts
            if alert["type"] == alert_type:
                alert_time = datetime.fromisoformat(alert["timestamp"])
                if (now - alert_time).total_seconds() < cooldown_period:
                    return False
        
        # Check for same node cooldown
        if node_id:
            node_cooldown = self.config["cooldown_periods"]["same_node"]
            for alert in reversed(self.alert_history[-20:]):
                if alert.get("node_id") == node_id:
                    alert_time = datetime.fromisoformat(alert["timestamp"])
                    if (now - alert_time).total_seconds() < node_cooldown:
                        return False
        
        return True
    
    def send_alert(self, alert):
        """Send alert through configured channels"""
        alert["timestamp"] = datetime.now().isoformat()
        
        # Add to history
        self.alert_history.append(alert)
        
        # Keep history manageable
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]
        
        # Send through each channel
        for channel in self.config["alert_channels"]:
            try:
                if channel == "console":
                    self._send_console_alert(alert)
                elif channel == "log":
                    self._send_log_alert(alert)
                elif channel == "email" and self.config["email_config"]["enabled"]:
                    self._send_email_alert(alert)
                elif channel == "telegram" and self.config["telegram_config"]["enabled"]:
                    self._send_telegram_alert(alert)
            except Exception as e:
                print(f"[ALERT] Error sending alert via {channel}: {e}")
        
        # Also add to active alerts if critical/high
        if alert["severity"] in ["CRITICAL", "HIGH"]:
            self.alerts.append(alert)
            if len(self.alerts) > 50:
                self.alerts = self.alerts[-50:]
    
    def _send_console_alert(self, alert):
        """Send alert to console"""
        colors = {
            "CRITICAL": "\033[91m",  # Red
            "HIGH": "\033[93m",      # Yellow
            "MEDIUM": "\033[94m",    # Blue
            "LOW": "\033[92m"        # Green
        }
        reset = "\033[0m"
        
        color = colors.get(alert["severity"], "\033[0m")
        
        print(f"\n{color}🚨 ALERT [{alert['severity']}]: {alert['message']}{reset}")
        if "data" in alert:
            print(f"   Data: {alert['data']}")
        print(f"   Time: {alert['timestamp']}")
    
    def _send_log_alert(self, alert):
        """Log alert to file"""
        log_entry = {
            "timestamp": alert["timestamp"],
            "type": alert["type"],
            "severity": alert["severity"],
            "message": alert["message"],
            "data": alert.get("data", {})
        }
        
        try:
            with open("alerts.log", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"[ALERT] Error logging alert: {e}")
    
    def _send_email_alert(self, alert):
        """Send alert via email"""
        config = self.config["email_config"]
        
        if not config["sender_email"] or not config["sender_password"]:
            return
        
        msg = MIMEMultipart()
        msg['From'] = config["sender_email"]
        msg['To'] = ", ".join(config["recipients"])
        msg['Subject'] = f"[{alert['severity']}] Blockchain Alert: {alert['type']}"
        
        body = f"""
        Blockchain Alert Detected:
        
        Type: {alert['type']}
        Severity: {alert['severity']}
        Message: {alert['message']}
        Time: {alert['timestamp']}
        
        Additional Data:
        {json.dumps(alert.get('data', {}), indent=2)}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
            server.starttls()
            server.login(config["sender_email"], config["sender_password"])
            server.send_message(msg)
            server.quit()
            print(f"[ALERT] Email sent to {len(config['recipients'])} recipients")
        except Exception as e:
            print(f"[ALERT] Email error: {e}")
    
    def _send_telegram_alert(self, alert):
        """Send alert via Telegram"""
        config = self.config["telegram_config"]
        
        if not config["bot_token"] or not config["chat_id"]:
            return
        
        message = f"""
🚨 *{alert['severity']} Alert*
*Type:* {alert['type']}
*Message:* {alert['message']}
*Time:* {alert['timestamp']}
        """
        
        if "data" in alert:
            message += f"\n*Data:*\n```\n{json.dumps(alert['data'], indent=2)}\n```"
        
        url = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage"
        payload = {
            "chat_id": config["chat_id"],
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code != 200:
                print(f"[ALERT] Telegram error: {response.text}")
        except Exception as e:
            print(f"[ALERT] Telegram error: {e}")
    
    def monitor_transactions(self, transactions):
        """Monitor a batch of transactions for alerts"""
        all_alerts = []
        
        for tx in transactions:
            if hasattr(tx, 'ai_score'):
                alerts = self.check_transaction_risk(tx, tx.ai_score)
                all_alerts.extend(alerts)
        
        # Send alerts
        for alert in all_alerts:
            if self.should_alert(alert["type"]):
                self.send_alert(alert)
        
        return all_alerts
    
    def get_active_alerts(self):
        """Get currently active alerts"""
        # Filter out alerts older than 24 hours
        cutoff = datetime.now() - timedelta(hours=24)
        cutoff_iso = cutoff.isoformat()
        
        active = [alert for alert in self.alerts if alert["timestamp"] > cutoff_iso]
        self.alerts = active  # Update list
        
        return active
    
    def acknowledge_alert(self, alert_id):
        """Acknowledge/remove an alert"""
        self.alerts = [alert for alert in self.alerts if alert.get("id") != alert_id]
    
    def start_monitoring(self, check_interval=30):
        """Start continuous monitoring in background thread"""
        if self.running:
            print("[ALERT] Monitoring already running")
            return
        
        self.running = True
        
        def monitor():
            print(f"[ALERT] Background monitoring started (interval: {check_interval}s)")
            while self.running:
                try:
                    # Check for active alerts that need reminders
                    self._check_alert_reminders()
                    time.sleep(check_interval)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"[ALERT] Monitor error: {e}")
                    time.sleep(check_interval)
        
        self.alert_thread = threading.Thread(target=monitor, daemon=True)
        self.alert_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.running = False
        if self.alert_thread:
            self.alert_thread.join(timeout=5)
        print("[ALERT] Monitoring stopped")
    
    def _check_alert_reminders(self):
        """Send reminders for unacknowledged critical alerts"""
        cutoff = datetime.now() - timedelta(minutes=30)
        cutoff_iso = cutoff.isoformat()
        
        for alert in self.alerts:
            if alert["severity"] == "CRITICAL" and alert["timestamp"] < cutoff_iso:
                # Resend critical alerts every 30 minutes
                print(f"[ALERT] Resending critical alert: {alert['type']}")
                self.send_alert(alert)
    
    def print_alert_summary(self):
        """Print summary of alerts"""
        active = self.get_active_alerts()
        total = len(self.alert_history)
        
        print("\n=== ALERT SYSTEM SUMMARY ===")
        print(f"Total alerts in history: {total}")
        print(f"Active alerts (last 24h): {len(active)}")
        
        if active:
            print("\nActive alerts:")
            for i, alert in enumerate(active[:5], 1):  # Show first 5
                print(f"{i}. [{alert['severity']}] {alert['type']}: {alert['message']}")
        
        # Count by severity
        severities = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for alert in self.alert_history[-100:]:  # Last 100 alerts
            severities[alert["severity"]] += 1
        
        print("\nRecent alerts by severity:")
        for severity, count in severities.items():
            if count > 0:
                print(f"  {severity}: {count}")

# Test function
def test_alert_system():
    print("\nTesting AI Alert System...")
    
    # Create alert system
    alert_system = AIAlertSystem("test_alert_config.json")
    
    # Test transaction alerts
    class TestTransaction:
        def __init__(self, tx_id, ai_score):
            self.tx_id = tx_id
            self.sender = "alice"
            self.receiver = "bob"
            self.amount = 1000
            self.ai_score = ai_score
    
    print("\n1. Testing transaction alerts...")
    transactions = [
        TestTransaction("tx_001", 0.9),  # High risk
        TestTransaction("tx_002", 0.3),  # Low risk
        TestTransaction("tx_003", 0.85), # High risk
    ]
    
    alerts = alert_system.monitor_transactions(transactions)
    print(f"Generated {len(alerts)} transaction alerts")
    
    # Test node health alerts
    print("\n2. Testing node health alerts...")
    node_metrics = {
        "cpu_percent": 95,
        "memory_percent": 85,
        "disk_free_percent": 5
    }
    
    health_alerts = alert_system.check_node_health(node_metrics)
    for alert in health_alerts:
        if alert_system.should_alert(alert["type"]):
            alert_system.send_alert(alert)
    
    print(f"Generated {len(health_alerts)} node health alerts")
    
    # Print summary
    print("\n3. Alert summary...")
    alert_system.print_alert_summary()
    
    print("\n✅ Alert system test completed!")

if __name__ == "__main__":
    test_alert_system()
