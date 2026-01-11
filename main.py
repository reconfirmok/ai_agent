import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAXIMUM_ITERATION


def main():
    parser = argparse.ArgumentParser(prog='Chatbot', description="ai agent using google gemini API")
    parser.add_argument("user_prompt", type=str, help="User prompt to send to the model")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(
        role="user",
        parts=[types.Part(text=user_prompt)]
        )]
    if args.verbose:
        print(f"User prompt: {user_prompt}")

    for i in range(MAXIMUM_ITERATION):
        try:
            final_result = generate_content(client, messages, args.verbose)
            if final_result:
                print("Final result:")
                print(final_result)
                return
        except Exception as e:
            print(f"Error: {e}")

    print(f"Max iteration {MAXIMUM_ITERATION} reached")
    sys.exit(1)



def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,
                                           temperature=0,
                                           tools=[available_functions])
    )

    if not response.usage_metadata:
        raise RuntimeError("Invalid response from Gemini API")
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_results = []
    for call in response.function_calls:
        result = call_function(call, verbose)
        if (not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
            ):
            raise Exception(f"Error: Empty response from {call.name}")
        
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_results.append(result.parts[0])

    messages.append(types.Content(role="user", parts=function_results))

if __name__ == "__main__":
    main()
