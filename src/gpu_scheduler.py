import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class Job:
    performance_tier: str

@dataclass
class GPU:
    type: str
    price: float

class GPUScheduler:
    def __init__(self, gpu_types: Dict[str, float]):
        self.gpu_types = gpu_types

    def select_gpu(self, job: Job) -> GPU:
        gpu_type = self._select_gpu_type(job.performance_tier)
        return GPU(gpu_type, self.gpu_types[gpu_type])

    def _select_gpu_type(self, performance_tier: str) -> str:
        # For simplicity, assume A100 is the most cost-effective for high-tier jobs
        if performance_tier == "high":
            return "A100"
        # For simplicity, assume V100 is the most cost-effective for low-tier jobs
        elif performance_tier == "low":
            return "V100"
        else:
            raise ValueError("Invalid performance tier")

    def calculate_cost_savings(self, job: Job, selected_gpu: GPU, original_price: float) -> float:
        selected_gpu_price = self.gpu_types[selected_gpu.type]
        cost_savings = (original_price - selected_gpu_price) / original_price
        return cost_savings

def main():
    gpu_types = {
        "A100": 10.0,
        "V100": 15.0
    }
    scheduler = GPUScheduler(gpu_types)

    job = Job("high")
    selected_gpu = scheduler.select_gpu(job)
    cost_savings = scheduler.calculate_cost_savings(job, selected_gpu, 15.0)

    print(f"Selected GPU: {selected_gpu.type}")
    print(f"Cost savings: {cost_savings * 100}%")

if __name__ == "__main__":
    main()
