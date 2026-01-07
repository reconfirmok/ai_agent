import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
        
        if os.path.commonpath([working_dir_abs_path, file_path_abs]) != working_dir_abs_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_path_abs, "r") as f:
            file_content = f.read(MAX_CHARS)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'