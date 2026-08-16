import os
from dotenv import load_dotenv
from groq import Groq 

load_dotenv()
my_key = os.environ.get('SECRET_KEY')

# DEBUG LINE: This prints what Python actually found
print(f"Debug: Loaded key is -> {my_key}")

client = Groq(api_key=my_key)

def ask_llm(text):
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {'role': 'user', 'content': text}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    user_input = input("Enter your prompt: ")
    reply = ask_llm(user_input)
    print(reply)