from monitoring import AlertManager, Job
import pytest
from datetime import datetime, timedelta

def test_send_alert():
    alert_manager = AlertManager()
    job = Job("job-1", "failure reason", "stack trace")
    alert_manager.send_alert("user-1", job, "https://example.com/webhook")
    assert alert_manager.last_alert_time["user-1"] is not None

def test_throttle_alert():
    alert_manager = AlertManager()
    job = Job("job-1", "failure reason", "stack trace")
    alert_manager.send_alert("user-1", job, "https://example.com/webhook")
    assert alert_manager.throttle_alert("user-1") is True

def test_throttle_alert_after_minute():
    alert_manager = AlertManager()
    job = Job("job-1", "failure reason", "stack trace")
    alert_manager.last_alert_time["user-1"] = datetime.now() - timedelta(minutes=2)
    assert alert_manager.throttle_alert("user-1") is False

def test_send_alert_multiple_times():
    alert_manager = AlertManager()
    job = Job("job-1", "failure reason", "stack trace")
    alert_manager.send_alert("user-1", job, "https://example.com/webhook")
    alert_manager.send_alert("user-1", job, "https://example.com/webhook")
    assert alert_manager.last_alert_time["user-1"] is not None
