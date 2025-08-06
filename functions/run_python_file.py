import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_dir = os.path.abspath(working_directory)
    abs_file_path =  os.path.abspath(os.path.join(working_directory,file_path))
    if not abs_file_path.startswith(abs_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    call = []
    call.append ("python3")
    call.append (abs_file_path)
    for arg in args:
        call.append (arg)
    print ('__________________________________')
    print ("Trying to call.."+str(call))

    to_return = ''
    try:
        result = subprocess.run(call,capture_output=True, timeout=30, text=True,cwd=abs_dir)

        if result.stdout:
            to_return += f"STDOUT: {result.stdout}"
        if result.stderr:
            to_return += f"STDERR: {result.stderr}"
        if result.returncode != 0:
            to_return += f"\nProcess exited with code {result.returncode}"
        if result.stdout == '':
            to_return += f"\nNo output produced"
    
        return to_return
        
    except Exception as e:
        return f"Eror: executing Python file: {e}"
    
    