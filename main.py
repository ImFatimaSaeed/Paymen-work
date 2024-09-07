import csv
import sys
import argparse
from simulation.greedy import run_greedy
from simulation.dispatching.dispatcher import Dispatchers  # Correct the import

# Ensure this is indented properly inside a function or remove it if unnecessary here.
# If this was meant to be in load_schedule(), keep it there instead of in main.py.
def load_schedule():
    with open('aco_cpu/schedule_output.txt', 'r') as file:
        # Add logic to process the file
        reader = csv.DictReader(file, delimiter='\t')
        schedule = [row for row in reader]
    return schedule

sys.path.insert(0, '.')

def main():
    # Initialize the parser
    parser = argparse.ArgumentParser()
    
    # Add arguments
    parser.add_argument('--dataset', type=str, default='SMT2020_HVLM')
    parser.add_argument('--days', type=int, default=1)
    parser.add_argument('--dispatcher', type=str, default='fifo')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--wandb', action='store_true', default=False)
    parser.add_argument('--chart', action='store_true', default=False)
    parser.add_argument('--alg', type=str, default='l4m', choices=['l4m', 'm4l'])
    
    args = parser.parse_args()

    profile = False
    if profile:
        from pyinstrument import Profiler # type: ignore
        p = Profiler()
        p.start()

    # Initialize time
    current_time = 0

    # Run the simulation
    run_greedy(args.dataset, args.days, args.dispatcher, args.seed, args.wandb, args.chart, args.alg)

    print("Completed.")

    if profile:
        p.stop()
        p.open_in_browser()

# Ensure the time is updated to the next event’s end time after processing each lot
def run_greedy(dataset, days, dispatcher, seed, wandb, chart, alg):
    current_time = 0  # Start time
    events_processed = 0

    for event in Dispatchers.load_schedule():  # Ensure this is called correctly
        # Process each event according to the schedule
        current_time = float(event['end_time'])  # Update current time to end of the current event
        events_processed += 1
        print(f"Processed event {events_processed} at time {current_time}")

if __name__ == "__main__":
    main()
