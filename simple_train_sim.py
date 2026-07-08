from pathlib import Path
from Simulation import Simulation

def main():
    config_path = Path('network_config.json')
    simulation = Simulation.from_json(config_path)
    events = simulation.run(max_time=60)

    print("Events")
    for event in events:
        print(event)

    simulation.print_summary()

if __name__ == '__main__':
    main()