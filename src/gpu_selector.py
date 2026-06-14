import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class PerformanceTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class GPUType:
    name: str
    price: float

class GPUSelector:
    def __init__(self, gpu_types: Dict[str, GPUType]):
        self.gpu_types = gpu_types

    def select_gpu(self, performance_tier: PerformanceTier) -> GPUType:
        if performance_tier == PerformanceTier.LOW:
            return min(self.gpu_types.values(), key=lambda gpu: gpu.price)
        elif performance_tier == PerformanceTier.MEDIUM:
            return sorted(self.gpu_types.values(), key=lambda gpu: gpu.price)[1]
        else:
            return max(self.gpu_types.values(), key=lambda gpu: gpu.price)

    def calculate_cost_savings(self, original_price: float, selected_gpu_price: float) -> float:
        return round((original_price - selected_gpu_price) / original_price * 100, 2)

def load_gpu_types() -> Dict[str, GPUType]:
    gpu_types = {
        "A100": GPUType("A100", 10.0),
        "V100": GPUType("V100", 5.0),
    }
    return gpu_types

def main():
    gpu_types = load_gpu_types()
    selector = GPUSelector(gpu_types)
    performance_tier = PerformanceTier.HIGH
    selected_gpu = selector.select_gpu(performance_tier)
    original_price = 15.0
    cost_savings = selector.calculate_cost_savings(original_price, selected_gpu.price)
    print(f"Selected GPU: {selected_gpu.name}")
    print(f"Cost savings: {cost_savings}%")

if __name__ == "__main__":
    main()
