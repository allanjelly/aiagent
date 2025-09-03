import sys
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.function_description import *
from functions.call_function import call_function


def main():
    print("Hello from aiagent!")

    if len(sys.argv) == 1:
        print ('Podaj prompt!')
        exit (1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    system_prompt = """You are a helpful AI coding agent.
                    When a user asks a question or makes a request, call required functions. You can perform the following operations:
                    - List files and directories
                    - Read file content
                    - Execute Python files with optional arguments
                    - Write or overwrite files
                    All paths you provide should be relative to the working directory.
                    Call the required functions and do not give the text response until you executed your plan.
                    First analyze the files you have in your working directory. Main calculator file is main.py"""
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
            ]
        )       

    user_prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

# main loop - call ai 20 times at max
    for i in range(1,20):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents= messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]))

# this is final response
        if not response.function_calls and response.text:
            print (f"Final response: {response.text}")
            quit()

# add response variants to conversation thread
        for response_variant in response.candidates:
            messages.append(response_variant.content)

# check if we have a function to call and call it 
        for function_call in response.function_calls:       
            try:
                function_response = call_function(function_call)
            except Function_call_error as err:
                print(err)

            if not function_response.parts[0].function_response.response:
                raise Exception ("No function response")
            else:           
# add results of function calls to conversation            
                messages.append(function_response)
            

if __name__ == "__main__":
    main()
