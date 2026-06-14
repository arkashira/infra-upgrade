import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class Job:
    performance_tier: str
    gpu_type: str = None
    cost: float = 0.0

class Scheduler:
    def __init__(self, spot_pricing: Dict[str, float]):
        self.spot_pricing = spot_pricing

    def select_gpu_type(self, job: Job) -> Job:
        gpu_types = {
            'low': 'V100',
            'medium': 'A100',
            'high': 'A100'
        }
        gpu_type = gpu_types.get(job.performance_tier, 'V100')
        job.gpu_type = gpu_type
        job.cost = self.spot_pricing.get(gpu_type, 0.0)
        return job

    def log_cost_savings(self, job: Job, original_cost: float) -> float:
        cost_savings = (original_cost - job.cost) / original_cost * 100
        if cost_savings >= 15:
            print(f'Cost savings: {cost_savings}%')
        return cost_savings
