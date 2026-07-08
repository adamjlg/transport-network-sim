from typing import Optional
from dataclasses import dataclass

@dataclass
class Edge:
    from_node: str
    to_node: str
    travel_time: int
    occupied_until: int = -1
    occupied_by: Optional[str] = None

    def is_available(self, current_time: int) -> bool:
        return current_time > self.occupied_until

    def reserve(self, train_id: str, current_time: int, headway: int) -> int:
        arrival_time = current_time + self.travel_time
        self.occupied_until = arrival_time + headway
        self.occupied_by = train_id
        return arrival_time