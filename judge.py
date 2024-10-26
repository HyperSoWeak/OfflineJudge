import argparse
import subprocess
import json
import os
import sys

executable_path = None

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
    if executable_path is not None:
        os.remove(executable_path)
    sys.exit(1)

class Result:
    def __init__(self):
        self.result = None

    def set(self, result):
        valid_results = ['AC', 'WA', 'RE', 'CE', 'TLE', 'MLE']
        if result not in valid_results:
            raise ValueError(f"Invalid result: {result}. Must be one of {valid_results}.")
        self.result = result

    def print(self):
        print("\nResult:")

        if self.result is None:
            error_exit("No result.")
        elif self.result == 'AC':
            self.ac()
        elif self.result == 'WA':
            self.wa()
        elif self.result == 'RE':
            self.re()
        elif self.result == 'CE':
            self.ce()
        elif self.result == 'TLE':
            self.tle()
        elif self.result == 'MLE':
            self.mle()

    def ac(self):
        cprint('green', """
 █████╗  ██████╗
██╔══██╗██╔════╝
███████║██║     
██╔══██║██║     
██║  ██║╚██████╗
╚═╝  ╚═╝ ╚═════╝
        """)

    def wa(self):
        cprint('red', """
██╗    ██╗ █████╗ 
██║    ██║██╔══██╗
██║ █╗ ██║███████║
██║███╗██║██╔══██║
╚███╔███╔╝██║  ██║
 ╚══╝╚══╝ ╚═╝  ╚═╝
        """)

    def re(self):
        cprint('cyan', """
██████╗ ███████╗
██╔══██╗██╔════╝
██████╔╝█████╗  
██╔══██╗██╔══╝  
██║  ██║███████╗
╚═╝  ╚═╝╚══════╝
        """)

    def ce(self):
        cprint('yellow', """
 ██████╗███████╗
██╔════╝██╔════╝
██║     █████╗  
██║     ██╔══╝  
╚██████╗███████╗
 ╚═════╝╚══════╝
        """)

    def tle(self):
        cprint('blue', """
████████╗██╗     ███████╗
╚══██╔══╝██║     ██╔════╝
   ██║   ██║     █████╗  
   ██║   ██║     ██╔══╝  
   ██║   ███████╗███████╗
   ╚═╝   ╚══════╝╚══════╝
        """)

    def mle(self):
        cprint('magenta', """
███╗   ███╗██╗     ███████╗
████╗ ████║██║     ██╔════╝
██╔████╔██║██║     █████╗  
██║╚██╔╝██║██║     ██╔══╝  
██║ ╚═╝ ██║███████╗███████╗
╚═╝     ╚═╝╚══════╝╚══════╝
        """)

class Judge():
    def __init__(self, problem_name, submission_file):
        self.problem_name = problem_name
        self.submission_file = submission_file
        self.problem_path = None
        self.submission_path = None

        self.problem_info = None
        self.result = Result()

    def run(self):
        problem_name = self.problem_name
        submission_file = self.submission_file
        
        self.problem_path = os.path.join(os.getcwd(), 'problems', problem_name)
        self.submission_path = os.path.join(os.getcwd(), 'submissions', submission_file)

        if not os.path.isdir(self.problem_path):
            error_exit(f"The problem '{problem_name}' does not exist in './problems'.")

        if not os.path.isfile(self.submission_path):
            error_exit(f"The file '{submission_file}' does not exist in './submissions'.")

        self.get_problem_info()

        print('\nProblem: ', end='')
        cprint('cyan', self.problem_info['title'])
        print()

        global executable_path
        executable_path = self.compile_cpp(self.submission_path)
        if executable_path is not None:
            self.judge_problem()

        self.result.print()
        self.cleanup()

    def get_problem_info(self):
        file_path = os.path.join(self.problem_path, 'problem.json')

        with open(file_path, 'r') as f:
            self.problem_info = json.load(f)

    def compile_cpp(self, file_path):
        max_error_length = 1000
        output_filename = os.path.splitext(file_path)[0]

        try:
            subprocess.run(
                ['g++', file_path, '-o', output_filename],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            cprint('green', 'Compilation successful.')

        except subprocess.CalledProcessError as e:
            self.result.set('CE')
            error_message = e.stderr.decode().strip()
            
            if len(error_message) > max_error_length:
                error_message = error_message[:max_error_length] + '... [output truncated]'

            cprint('red', 'Compilation failed with error:')
            print(error_message)
            return None

        return output_filename

    def judge_problem(self):
        global executable_path
        problem_path = self.problem_path
        print("Judging...")

    def cleanup(self):
        global executable_path
        if executable_path is not None:
            os.remove(executable_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Judge a problem submission.", 
                                     usage="python judge.py [problem_name] [submission_file]")
    
    parser.add_argument("problem_name", type=str, help="The name of the problem to be judged")
    parser.add_argument("submission_file", type=str, help="The filename of the submission to be judged")

    args = parser.parse_args()

    judge = Judge(args.problem_name, args.submission_file)
    judge.run()
