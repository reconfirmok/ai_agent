import os

from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
        
        if os.path.commonpath([working_dir_abs_path, file_path_abs]) != working_dir_abs_path:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)

        with open(file_path_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing file "{file_path}": {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to read content from, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content that will be written to the file"
            )
        },
        required=["file_path", "content"]
    ),
)