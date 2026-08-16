def greet():
    print("Hello")
greet()

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_key = os.environ.get('SECRET_KEY')

client = Groq(api_key=my_key)


def ask_llm(text):
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {'role': 'system', 'content': 'You are a professional summarizer. Summarize the text you are given clearly and concisely, keeping only the key points.'},
            {'role': 'user', 'content': text}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    user_input = input("Paste text to summarize: ")
    reply = ask_llm(user_input)
    print(reply)