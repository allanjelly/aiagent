Uses google genai api to perform simple tasks.
It can repair simple bugs in python code.
You call it like:    python2 main.py "Can you repair the calculator located in calculator/main.py 3+7*2 should not be 20" --verbose
It calls genai api - which returns functions to call (schema contains read_files_info, read_file_content, write_file, execute_file).
Results of f.calls are added to the conversation and returned to google until bug is repaired.
