# tests/test_benchmark_run.py
from pathlib import Path
import pytest
from simulation import Simulation

SCENARIOS= [
    Path("tests/scenarios/small_linear.json"),
    Path("tests/scenarios/medium_shared_corridor.json"),
    Path("tests/scenarios/large_branching.json"),
]

@pytest.mark.parametrize("config_path", SCENARIOS, ids=lambda p: p.stem)
def test_benchmark_run_scenarios(benchmark, config_path):
    def run_sim():
        sim = Simulation.from_json(config_path)
        return sim.run(max_time=120)

    events = benchmark(run_sim)
    assert len(events) > 0