import time
import json
from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    id: int
    status: str

class AutoScaler:
    def __init__(self, max_nodes: int, scale_up_threshold: int, scale_down_threshold: int):
        self.max_nodes = max_nodes
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.nodes = []
        self.queue_length = 0
        self.last_scale_down_time = time.time()

    def update_queue_length(self, queue_length: int):
        self.queue_length = queue_length

    def scale_up(self):
        if len(self.nodes) < self.max_nodes and self.queue_length > self.scale_up_threshold:
            new_node = Node(id=len(self.nodes) + 1, status="running")
            self.nodes.append(new_node)
            print(f"Scaling up: Added node {new_node.id}")

    def scale_down(self):
        if self.nodes and self.queue_length == 0 and time.time() - self.last_scale_down_time > self.scale_down_threshold * 60:
            node_to_remove = self.nodes.pop(0)
            print(f"Scaling down: Removed node {node_to_remove.id}")
            self.last_scale_down_time = time.time()

    def run(self):
        while True:
            self.scale_up()
            self.scale_down()
            time.sleep(1)

def main():
    scaler = AutoScaler(max_nodes=8, scale_up_threshold=3, scale_down_threshold=10)
    scaler.update_queue_length(4)
    scaler.run()

if __name__ == "__main__":
    main()
