import subprocess


if __name__ == "__main__":
    process = subprocess.Popen(
        ['python', 'manage.py', 'process_tasks'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
