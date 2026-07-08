import json
from typing import List
from edge import Edge
from node import Node
from train import Train
from network import Network
from validation_error import ValidationError

class Simulation:
    def __init__(self, network, trains, headway):
        self.network = network
        self.trains = trains
        self.headway = headway
        self.events = []

    def validate(self):
        if self.headway < 0:
            raise ValidationError('Headway must be non-negative')
        if not self.network.nodes:
            raise ValidationError('Network must contain at least one node')
        if not self.network.edges:
            raise ValidationError('Network must contain at least one edge')
        if not self.trains:
            raise ValidationError('Simulation must contain at least one train')

        for train in self.trains:
            if not train.id:
                raise ValidationError('Train id is required')
            if len(train.route) < 2:
                raise ValidationError(f'Train {train.id} route must contain at least two nodes')
            if train.start_time < 0:
                raise ValidationError(f'Train {train.id} start_time must be non-negative')
            if train.dwell < 0:
                raise ValidationError(f'Train {train.id} dwell must be non-negative')

            for node_name in train.route:
                if node_name not in self.network.nodes:
                    raise ValidationError(f'Train {train.id} references unknown node {node_name}')

            for i in range(len(train.route) - 1):
                self.network.get_edge(train.route[i], train.route[i + 1])

        for edge in self.network.edges.values():
            if edge.travel_time <= 0:
                raise ValidationError(f'Edge {edge.from_node}->{edge.to_node} must have positive travel time')
            if edge.from_node not in self.network.nodes:
                raise ValidationError(f'Edge references unknown from_node {edge.from_node}')
            if edge.to_node not in self.network.nodes:
                raise ValidationError(f'Edge references unknown to_node {edge.to_node}')

    def log_event(self, time: int, train_id: str, event: str, from_node: str, to_node: str, detail: str):
        self.events.append({
            'time': time,
            'train_id': train_id,
            'event': event,
            'from_node': from_node,
            'to_node': to_node,
            'detail': detail,
        })

    def run(self, max_time: int = 60):
        self.validate()

        for t in range(max_time + 1):
            for train in self.trains:
                if train.completed or t < train.ready_time:
                    continue

                if train.at_final_node():
                    train.completed = True
                    train.status = 'completed'
                    self.log_event(
                        t,
                        train.id,
                        'complete_service',
                        train.route[-1],
                        '',
                        f'Completed route with total delay {train.delay}'
                    )
                    continue

                current_node = train.current_node()
                next_node = train.next_node()
                edge = self.network.get_edge(current_node, next_node)

                if edge.is_available(t):
                    arrival_time = edge.reserve(train.id, t, self.headway)
                    train.route_index += 1
                    train.ready_time = arrival_time + train.dwell
                    train.status = f'arriving_{next_node}'

                    self.log_event(
                        t,
                        train.id,
                        'depart_edge',
                        current_node,
                        next_node,
                        f'Travel time {edge.travel_time} min; edge reserved until {edge.occupied_until}'
                    )
                    self.log_event(
                        arrival_time,
                        train.id,
                        'arrive_node',
                        current_node,
                        next_node,
                        f'Dwell until {train.ready_time}'
                    )
                else:
                    train.delay += 1
                    train.ready_time = t + 1
                    train.status = f'waiting_for_{current_node}_{next_node}'
                    self.log_event(
                        t,
                        train.id,
                        'blocked_by_headway',
                        current_node,
                        next_node,
                        f'Edge occupied by {edge.occupied_by} until {edge.occupied_until}'
                    )

        return self.events

    def print_summary(self):
        print('Summary')
        for train in self.trains:
            print(train.id, train.delay, train.completed, train.status)


    @classmethod
    def from_json(cls, path):
        with open(path, "r") as f:
            config = json.load(f)

        nodes = {name: Node(name=name) for name in config["nodes"]}

        edges = {}
        for edge_data in config["edges"]:
            edge = Edge(
                from_node=edge_data["from"],
                to_node=edge_data["to"],
                travel_time=edge_data["travel_time"],
            )
            edges[(edge.from_node, edge.to_node)] = edge

        trains = []
        for train_data in config["trains"]:
            trains.append(
                Train(
                    id=train_data.get("id", ""),
                    route=train_data.get("route", []),
                    start_time=train_data.get("start_time", -1),
                    dwell=train_data.get("dwell", 1),
                )
            )

        network = Network(nodes=nodes, edges=edges)
        return cls(network=network, trains=trains, headway=config["headway"])