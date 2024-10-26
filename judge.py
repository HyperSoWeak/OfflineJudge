import argparse
import subprocess
import os
import sys

def ac():
    cprint('green', """
 █████╗  ██████╗
██╔══██╗██╔════╝
███████║██║     
██╔══██║██║     
██║  ██║╚██████╗
╚═╝  ╚═╝ ╚═════╝
    """)

def wa():
    cprint('red', """
██╗    ██╗ █████╗ 
██║    ██║██╔══██╗
██║ █╗ ██║███████║
██║███╗██║██╔══██║
╚███╔███╔╝██║  ██║
 ╚══╝╚══╝ ╚═╝  ╚═╝
    """)

def re():
    cprint('cyan', """
██████╗ ███████╗
██╔══██╗██╔════╝
██████╔╝█████╗  
██╔══██╗██╔══╝  
██║  ██║███████╗
╚═╝  ╚═╝╚══════╝
    """)

def ce():
    cprint('yellow', """
 ██████╗███████╗
██╔════╝██╔════╝
██║     █████╗  
██║     ██╔══╝  
╚██████╗███████╗
 ╚═════╝╚══════╝
    """)

def tle():
    cprint('blue', """
████████╗██╗     ███████╗
╚══██╔══╝██║     ██╔════╝
   ██║   ██║     █████╗  
   ██║   ██║     ██╔══╝  
   ██║   ███████╗███████╗
   ╚═╝   ╚══════╝╚══════╝
    """)

def mle():
    cprint('magenta', """
███╗   ███╗██╗     ███████╗
████╗ ████║██║     ██╔════╝
██╔████╔██║██║     █████╗  
██║╚██╔╝██║██║     ██╔══╝  
██║ ╚═╝ ██║███████╗███████╗
╚═╝     ╚═╝╚══════╝╚══════╝
    """)


def cprint(color, *args, **kwargs):
    color_codes = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
        'reset': '0',
    }
    
    ansi_code = color_codes.get(color, '37')    
    colored_text = f"\033[{ansi_code}m" + ' '.join(map(str, args)) + f"\033[0m"
    print(colored_text, **kwargs)

def error_exit(message):
    cprint('red', 'Error: ', end='')
    print(message)
    sys.exit(1)

def compile_cpp(file_path):
    if not os.path.isfile(file_path):
        print(f"\033[91mError: The file '{file_path}' does not exist.\033[0m")
        return None
    
    output_filename = os.path.splitext(file_path)[0]

    try:
        result = subprocess.run(
            ['g++', file_path, '-o', output_filename],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Compilation successful. Executable created: {output_filename}")

    except subprocess.CalledProcessError as e:
        ce()
        print(f"\033[91mCompilation failed with error:\033[0m\n{e.stderr.decode().strip()}")
        return None

    return output_filename

def judge_problem(problem_name, submission_file):
    problem_path = os.path.join(os.getcwd(), 'problems', problem_name)
    submission_path = os.path.join(os.getcwd(), 'submissions', submission_file)

    if not os.path.isdir(problem_path):
        error_exit(f"The problem '{problem_name}' does not exist in './problems'.")

    compile_cpp(submission_path)

    print(f"Judging the problem: {problem_name}")
    print(f"Submission file: {submission_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Judge a problem submission.", 
                                     usage="python judge.py [problem_name] [submission_file]")
    
    parser.add_argument("problem_name", type=str, help="The name of the problem to be judged")
    parser.add_argument("submission_file", type=str, help="The filename of the submission to be judged")

    args = parser.parse_args()

    ac()
    wa()
    re()
    ce()
    tle()
    mle()
    
    judge_problem(args.problem_name, args.submission_file)
