import os
import time
import random

def run_test_case(test_case_id):
    """Simulates running a test case and returns the result and runtime."""
    # Simulate a random runtime between 0.1 to 2 seconds
    runtime = round(random.uniform(0.1, 2.0), 2)
    time.sleep(runtime)  # Simulate the time taken to run the test case

    # Simulate a random result: AC, WA, RE, etc.
    result = random.choice(['AC', 'WA', 'RE', 'TLE', 'MLE'])
    
    return result, runtime

def display_test_case_results(test_cases):
    """Displays the results for each test case."""
    print(f"{'Test Case ID':<15} {'Runtime (s)':<15} {'Result':<5}")
    print("-" * 40)

    for test_case_id in test_cases:
        result, runtime = run_test_case(test_case_id)
        print(f"{test_case_id:<15} {runtime:<15} {result:<5}")

if __name__ == "__main__":
    # Example test case IDs, could be populated from files or other sources
    test_case_ids = [f"{i:02}" for i in range(1, 11)]  # e.g., '01', '02', ..., '10'

    display_test_case_results(test_case_ids)
