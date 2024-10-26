import argparse
import subprocess
import difflib
import json
import os
import sys
import time

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
    judge.cleanup()
    sys.exit(1)

class Result:
    def __init__(self):
        self.result = None
        self.score = 0
        self.max_score = 100

    def set_result(self, result):
        if self.result is None:
            self.result = result

    def get_result(self):
        return self.result
    
    def add_score(self, score):
        self.score += score

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

        print('Score: ', end='')
        cprint('yellow', f'{self.score} / {self.max_score}')

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
        self.executable_path = None

        self.output_path = os.path.join(os.path.dirname(__file__), 'submissions/user.out')

        self.problem_info = None
        self.subtask_info = None
        self.result = Result()

    def run(self):
        os.system("clear")

        problem_name = self.problem_name
        submission_file = self.submission_file
        
        self.problem_path = os.path.join(os.path.dirname(__file__), 'problems', problem_name)
        self.submission_path = os.path.join(os.path.dirname(__file__), 'submissions', submission_file)

        if not os.path.isdir(self.problem_path):
            error_exit(f"The problem '{problem_name}' does not exist in './problems'.")
        if not os.path.isfile(self.submission_path):
            error_exit(f"The file '{submission_file}' does not exist in './submissions'.")

        self.get_problem_info()

        print('\nProblem: ', end='')
        cprint('cyan', self.problem_info['title'])
        print()

        self.executable_path = self.compile_cpp(self.submission_path)
        if self.executable_path is not None:
            self.judge_problem()

        self.result.print()
        self.cleanup()

    def get_problem_info(self):
        problem_path = os.path.join(self.problem_path, 'problem.json')
        subtask_path = os.path.join(self.problem_path, 'subtasks.json')

        with open(problem_path, 'r') as f:
            self.problem_info = json.load(f)
        with open(subtask_path, 'r') as f:
            self.subtask_info = json.load(f)

    def compile_cpp(self, file_path):
        max_error_length = 1000
        output_path = os.path.splitext(file_path)[0]

        print("Compiling...")

        try:
            subprocess.run(
                ['g++', file_path, '-o', output_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            cprint('green', 'Compilation successful.')

        except subprocess.CalledProcessError as e:
            self.result.set_result('CE')
            error_message = e.stderr.decode().strip()
            
            if len(error_message) > max_error_length:
                error_message = error_message[:max_error_length] + '... [output truncated]'

            cprint('red', 'Compilation failed with error:')
            print(error_message)
            return None

        return output_path

    def judge_problem(self):
        print("Judging...\n")
        
        print(f"{'Testcase':<10} {'Runtime':<10} {'Result':<10}")
        print("-" * 40)

        sorted_info = sorted(self.subtask_info['subtasks'].items(), key=lambda x: x[1]['index'])
        subtasks = {k: v for k, v in sorted_info}
        
        for name, info in subtasks.items():
            cprint('magenta', f"Subtask {info['index']} - {name}:")
            subtask = self.get_subtask(info['index'])
            
            ac = True
            for testcase in subtask:
                if not self.run_testcase(testcase):
                    ac = False

            if ac:
                self.result.add_score(info['score'])

        self.result.set_result('AC')

    def get_subtask(self, index):
        subtask = []
        tests_dir = os.path.join(self.problem_path, 'tests')

        for filename in os.listdir(tests_dir):
            if filename.startswith(f"{index}-") and filename.endswith('.in'):
                subtask.append({
                    'name': filename.replace('.in', ''),
                    'input': os.path.join(tests_dir, filename),
                    'output': os.path.join(tests_dir, filename.replace('.in', '.out'))
                })
        
        return sorted(subtask, key=lambda x: x['name'])

    def run_testcase(self, testcase):
        r = {
            'AC': '\033[32mAccepted\033[0m',
            'WA': '\033[31mWrong Answer\033[0m',
            'RE': '\033[36mRuntime Error\033[0m',
            'TLE': '\033[34mTime Limit Exceeded\033[0m',
            'MLE': '\033[35mMemory Limit Exceeded\033[0m'
        }

        result, runtime = self.execute(testcase['input'], self.output_path, testcase['output'])

        if result == 'TLE':
            self.result.set_result('TLE')
        elif result == 'WA':
            self.result.set_result('WA')

        print(f"{testcase['name']:<10} {runtime:<10} {r[result]:<10}")

        return result == 'AC'

    def execute(self, input_file, output_file, answer_file):
        # TODO: Implement TLE, MLE and RE handling
        # TODO: Multithreading
        # FIXME: Maybe use CPU time instead of wall time

        time_limit = self.problem_info['time_limit']
        start_time = time.time()

        try:
            with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
                subprocess.run([self.executable_path], stdin=infile, stdout=outfile, check=True, timeout=time_limit)
        except subprocess.TimeoutExpired:
            return ('TLE', time_limit)

        end_time = time.time()
        runtime = round(end_time - start_time, 3)

        diff = self.compare_output(self.output_path, answer_file)
        if diff:
            return ('WA', runtime)
        
        return ('AC', runtime)

    def compare_output(self, output_file, answer_file):
        with open(output_file, 'r') as out, open(answer_file, 'r') as ans:
            output_lines = self.normalize_output(out.readlines())
            answer_lines = self.normalize_output(ans.readlines())

        diff = list(difflib.unified_diff(output_lines, answer_lines, fromfile='output', tofile='expected'))
        return diff

    def normalize_output(self, output):
        return [line.rstrip() for line in output]

    def cleanup(self):
        if self.executable_path is not None:
            os.remove(self.executable_path)
        if os.path.isfile(self.output_path):
            os.remove(self.output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Judge a problem submission.", 
                                     usage="python judge.py [problem_name] [submission_file]")
    
    parser.add_argument("problem_name", type=str, help="The name of the problem to be judged")
    parser.add_argument("submission_file", type=str, help="The filename of the submission to be judged")

    args = parser.parse_args()

    judge = Judge(args.problem_name, args.submission_file)
    judge.run()
