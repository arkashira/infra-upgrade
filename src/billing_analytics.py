import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Job:
    id: int
    gpu_hours: float
    start_time: str
    spot_price: float

class BillingAnalytics:
    def __init__(self, jobs: List[Job]):
        self.jobs = jobs

    def calculate_costs(self):
        costs = []
        cumulative_spend = 0
        for job in self.jobs:
            cost = job.gpu_hours * job.spot_price
            cumulative_spend += cost
            costs.append({
                'job_id': job.id,
                'cost_per_gpu_hour': job.spot_price,
                'cost': cost,
                'cumulative_spend': cumulative_spend
            })
        return costs

    def export_to_csv(self, costs):
        with open('billing_analytics.csv', 'w') as f:
            f.write('Job ID,Cost per GPU hour,Cost,Cumulative Spend\n')
            for cost in costs:
                f.write(f"{cost['job_id']},{cost['cost_per_gpu_hour']},{cost['cost']},{cost['cumulative_spend']}\n")

def main():
    jobs = [
        Job(1, 10, '2022-01-01 12:00:00', 0.5),
        Job(2, 20, '2022-01-02 12:00:00', 0.6),
        Job(3, 30, '2022-01-03 12:00:00', 0.7)
    ]
    analytics = BillingAnalytics(jobs)
    costs = analytics.calculate_costs()
    analytics.export_to_csv(costs)
    print(costs)

if __name__ == '__main__':
    main()
