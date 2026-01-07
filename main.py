import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


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

    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages
    )

    if not response.usage_metadata:
        raise RuntimeError("Invalid response from Gemini API")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
