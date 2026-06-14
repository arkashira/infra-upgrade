import pytest
import time
from autoscaler import AutoScaler, Node

def test_scale_up():
    scaler = AutoScaler(max_nodes=8, scale_up_threshold=3, scale_down_threshold=10)
    scaler.update_queue_length(4)
    scaler.scale_up()
    assert len(scaler.nodes) == 1

def test_scale_down():
    scaler = AutoScaler(max_nodes=8, scale_up_threshold=3, scale_down_threshold=10)
    scaler.update_queue_length(0)
    scaler.nodes = [Node(id=1, status="running")]
    scaler.last_scale_down_time = time.time() - 600  # 10 minutes ago
    scaler.scale_down()
    assert len(scaler.nodes) == 0

def test_scale_up_multiple_nodes():
    scaler = AutoScaler(max_nodes=8, scale_up_threshold=3, scale_down_threshold=10)
    scaler.update_queue_length(4)
    for _ in range(7):
        scaler.scale_up()
    assert len(scaler.nodes) == 7

def test_scale_down_empty_queue():
    scaler = AutoScaler(max_nodes=8, scale_up_threshold=3, scale_down_threshold=10)
    scaler.update_queue_length(0)
    scaler.nodes = [Node(id=1, status="running")]
    scaler.scale_down()
    assert len(scaler.nodes) == 1

def test_scale_down_after_timeout():
    scaler = AutoScaler(max_nodes=8, scale_up_threshold=3, scale_down_threshold=10)
    scaler.update_queue_length(0)
    scaler.nodes = [Node(id=1, status="running")]
    scaler.last_scale_down_time = time.time() - 600  # 10 minutes ago
    scaler.scale_down()
    assert len(scaler.nodes) == 0
