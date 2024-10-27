import subprocess
import time
import os

def get_memory_usage(pid):
    """Get memory usage of the given process."""
    try:
        with open(f"/proc/{pid}/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1])  # Return memory in kB
    except FileNotFoundError:
        return 0

def run_cpp_program_and_monitor_memory(cpp_program, *args):
    """Run a C++ program and monitor its memory usage."""
    # Start the C++ program
    process = subprocess.Popen([cpp_program] + list(args))
    
    # Monitor memory usage
    memory_usage = []
    while True:
        # Get current memory usage
        mem_usage = get_memory_usage(process.pid)
        if mem_usage > 0:
            memory_usage.append(mem_usage)

        # Check if the process has finished
        if process.poll() is not None:
            break

        time.sleep(0.1)  # Adjust the sleep time as needed

    # Return the peak memory usage in kilobytes
    return max(memory_usage)

# Example usage
if __name__ == "__main__":
    cpp_program_path = "./test.cpp"  # Replace with your C++ program path
    peak_memory = run_cpp_program_and_monitor_memory(cpp_program_path, "arg1", "arg2")
    print(f"Peak Memory Usage: {peak_memory / 1024:.2f} MB")  # Convert kB to MB
