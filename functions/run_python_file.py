import subprocess
import os

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
        
        if os.path.commonpath([working_dir_abs_path, file_path_abs]) != working_dir_abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path_abs.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", file_path_abs]

        if args:
            command.extend(args)
        
        process = subprocess.run(command,
                                 cwd=working_dir_abs_path,
                                 capture_output=True,
                                 text=True,
                                 timeout=30)
        process_output = []

        if process.returncode != 0:
            process_output.append(f"Process exited with code {process.returncode}")
        if not process.stdout and not process.stderr:
            process_output.append("No output produced")
        if process.stdout:
            process_output.append(f"STDOUT:\n{process.stdout}")
        if process.stderr:
            process_output.append(f"STDERR:\n{process.stderr}")
        
        return "\n".join(process_output)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run a python file in a specified directory relative to the working directory, with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path for the python file to execute, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="the optional arguments passed to the function"
            ),
        },
        required=["file_path", "args"]
    ),
)