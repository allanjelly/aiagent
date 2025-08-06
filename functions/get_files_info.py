import os

def get_files_info(working_directory, directory="."):
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    abs_working = os.path.abspath(working_directory)
    if not abs_directory.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'

    ls = os.listdir(abs_directory)
    response = []
    response.append('------------')
    response.append(abs_directory)

    for file in ls:
        try:
            file_path = os.path.join(abs_directory,file)
            response.append(f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
        except Exception as e:
            response.append(f"Error: {e}")
    response_string = '\n'.join(response)

    return response_string
