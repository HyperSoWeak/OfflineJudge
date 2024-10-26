import subprocess
import os
import difflib

def compile_cpp(cpp_file, executable):
    """Compiles the given C++ file."""
    try:
        subprocess.run(["g++", cpp_file, "-o", executable], check=True)
        print(f"Compiled {cpp_file} successfully.")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to compile {cpp_file}.")
        return False

def run_executable(executable, input_file, output_file):
    """Runs the compiled executable with input and saves the output."""
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            subprocess.run([f"./{executable}"], stdin=infile, stdout=outfile, check=True)
        print(f"Executed {executable} successfully.")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to execute {executable}.")
        return False

def normalize_output(output):
    """Strips trailing spaces and newlines from each line in the output."""
    return [line.rstrip() for line in output]

def compare_output(output_file, answer_file):
    """Compares the output with the expected answer while ignoring trailing spaces and newlines."""
    with open(output_file, 'r') as out, open(answer_file, 'r') as ans:
        output_lines = normalize_output(out.readlines())
        answer_lines = normalize_output(ans.readlines())

    diff = list(difflib.unified_diff(output_lines, answer_lines, fromfile='output', tofile='expected'))
    
    if not diff:
        print("Output matches the expected result.")
        return True
    else:
        print("Output differs from the expected result:")
        for line in diff:
            print(line, end='')
        return False

def judge(cpp_file, input_file, answer_file):
    executable = "a.out"
    output_file = "output.txt"

    if not compile_cpp(cpp_file, executable):
        return

    if not run_executable(executable, input_file, output_file):
        return

    compare_output(output_file, answer_file)

    # Clean up the generated files
    os.remove(executable)
    os.remove(output_file)

# Example usage:
cpp_file = "sol.cpp"
input_file = "1.in"
answer_file = "1.out"

judge(cpp_file, input_file, answer_file)
