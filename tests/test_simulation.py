# tests/test_simulation.py
import pytest
from pathlib import Path
from simulation import Simulation

def test_run_completes_simple_scenario():
    sim = Simulation.from_json(Path("network_config.json"))
    events = sim.run(max_time=60)

    assert len(events) > 0
    assert any(event["event"] == "complete_service" for event in events)