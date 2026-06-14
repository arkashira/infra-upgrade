from billing_analytics import BillingAnalytics, Job
import pytest
import os

def test_calculate_costs():
    jobs = [
        Job(1, 10, '2022-01-01 12:00:00', 0.5),
        Job(2, 20, '2022-01-02 12:00:00', 0.6),
        Job(3, 30, '2022-01-03 12:00:00', 0.7)
    ]
    analytics = BillingAnalytics(jobs)
    costs = analytics.calculate_costs()
    assert len(costs) == 3
    assert costs[0]['cost'] == 5.0
    assert costs[1]['cost'] == 12.0
    assert costs[2]['cost'] == 21.0
    assert costs[0]['cumulative_spend'] == 5.0
    assert costs[1]['cumulative_spend'] == 17.0
    assert costs[2]['cumulative_spend'] == 38.0

def test_export_to_csv():
    jobs = [
        Job(1, 10, '2022-01-01 12:00:00', 0.5),
        Job(2, 20, '2022-01-02 12:00:00', 0.6),
        Job(3, 30, '2022-01-03 12:00:00', 0.7)
    ]
    analytics = BillingAnalytics(jobs)
    costs = analytics.calculate_costs()
    analytics.export_to_csv(costs)
    assert os.path.exists('billing_analytics.csv')
    with open('billing_analytics.csv', 'r') as f:
        lines = f.readlines()
        assert len(lines) == 4
        assert lines[0].strip() == 'Job ID,Cost per GPU hour,Cost,Cumulative Spend'
        assert lines[1].strip() == '1,0.5,5.0,5.0'
        assert lines[2].strip() == '2,0.6,12.0,17.0'
        assert lines[3].strip() == '3,0.7,21.0,38.0'
    os.remove('billing_analytics.csv')

def test_main():
    # This test is just to ensure the main function runs without errors
    from billing_analytics import main
    main()
