import pytest
from infra_upgrade import Job, Scheduler

def test_select_gpu_type():
    spot_pricing = {
        'V100': 1.0,
        'A100': 1.5
    }
    scheduler = Scheduler(spot_pricing)
    job = Job('low')
    job = scheduler.select_gpu_type(job)
    assert job.gpu_type == 'V100'

def test_log_cost_savings():
    spot_pricing = {
        'V100': 1.0,
        'A100': 1.5
    }
    scheduler = Scheduler(spot_pricing)
    job = Job('low')
    job = scheduler.select_gpu_type(job)
    original_cost = 2.0
    cost_savings = scheduler.log_cost_savings(job, original_cost)
    assert cost_savings >= 15

def test_job_submission():
    spot_pricing = {
        'V100': 1.0,
        'A100': 1.5
    }
    scheduler = Scheduler(spot_pricing)
    job = Job('medium')
    job = scheduler.select_gpu_type(job)
    assert job.gpu_type == 'A100'
