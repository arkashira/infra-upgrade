import pytest
from gpu_selector import GPUSelector, PerformanceTier, GPUType

def test_select_gpu_low():
    gpu_types = {
        "A100": GPUType("A100", 10.0),
        "V100": GPUType("V100", 5.0),
    }
    selector = GPUSelector(gpu_types)
    selected_gpu = selector.select_gpu(PerformanceTier.LOW)
    assert selected_gpu.name == "V100"

def test_select_gpu_medium():
    gpu_types = {
        "A100": GPUType("A100", 10.0),
        "V100": GPUType("V100", 5.0),
        "P100": GPUType("P100", 7.5),
    }
    selector = GPUSelector(gpu_types)
    selected_gpu = selector.select_gpu(PerformanceTier.MEDIUM)
    assert selected_gpu.name == "P100"

def test_select_gpu_high():
    gpu_types = {
        "A100": GPUType("A100", 10.0),
        "V100": GPUType("V100", 5.0),
    }
    selector = GPUSelector(gpu_types)
    selected_gpu = selector.select_gpu(PerformanceTier.HIGH)
    assert selected_gpu.name == "A100"

def test_calculate_cost_savings():
    gpu_types = {
        "A100": GPUType("A100", 10.0),
        "V100": GPUType("V100", 5.0),
    }
    selector = GPUSelector(gpu_types)
    original_price = 15.0
    selected_gpu_price = 10.0
    cost_savings = selector.calculate_cost_savings(original_price, selected_gpu_price)
    assert cost_savings == 33.33

def test_cost_savings_at_least_15_percent():
    gpu_types = {
        "A100": GPUType("A100", 10.0),
        "V100": GPUType("V100", 5.0),
    }
    selector = GPUSelector(gpu_types)
    original_price = 15.0
    selected_gpu_price = 12.75
    cost_savings = selector.calculate_cost_savings(original_price, selected_gpu_price)
    assert cost_savings >= 15.0
