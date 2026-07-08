from pathlib import Path
from transport_network_sim.simulation import Simulation

def main():
    config_path = Path('src/transport_network_sim/network_config.json')
    simulation = Simulation.from_json(config_path)
    events = simulation.run(max_time=60)

    print("Events")
    for event in events:
        print(event)

    simulation.print_summary()

if __name__ == '__main__':
    main()

    