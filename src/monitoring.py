import json
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict

@dataclass
class Job:
    id: str
    failure_reason: str
    stack_trace: str

class AlertManager:
    def __init__(self):
        self.last_alert_time: Dict[str, datetime] = {}

    def send_alert(self, user_id: str, job: Job, webhook_url: str):
        if user_id not in self.last_alert_time or datetime.now() - self.last_alert_time[user_id] > timedelta(minutes=1):
            self.last_alert_time[user_id] = datetime.now()
            alert = {
                "job_id": job.id,
                "failure_reason": job.failure_reason,
                "stack_trace": job.stack_trace
            }
            # Simulate sending alert to Slack channel via webhook
            print(f"Sending alert to user {user_id} via webhook {webhook_url}: {json.dumps(alert)}")

    def throttle_alert(self, user_id: str):
        if user_id in self.last_alert_time and datetime.now() - self.last_alert_time[user_id] < timedelta(minutes=1):
            return True
        return False
