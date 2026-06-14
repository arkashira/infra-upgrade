import pytest
from gpu_scheduler import Job, GPUScheduler, GPU

def test_select_gpu():
    gpu_types = {
        "A100": 10.0,
        "V100": 15.0
    }
    scheduler = GPUScheduler(gpu_types)

    job = Job("high")
    selected_gpu = scheduler.select_gpu(job)
    assert selected_gpu.type == "A100"

    job = Job("low")
    selected_gpu = scheduler.select_gpu(job)
    assert selected_gpu.type == "V100"

def test_calculate_cost_savings():
    gpu_types = {
        "A100": 10.0,
        "V100": 15.0
    }
    scheduler = GPUScheduler(gpu_types)

    job = Job("high")
    selected_gpu = GPU("A100", 10.0)
    cost_savings = scheduler.calculate_cost_savings(job, selected_gpu, 15.0)
    assert cost_savings >= 0.15

def test_invalid_performance_tier():
    gpu_types = {
        "A100": 10.0,
        "V100": 15.0
    }
    scheduler = GPUScheduler(gpu_types)

    job = Job("invalid")
    with pytest.raises(ValueError):
        scheduler.select_gpu(job)
