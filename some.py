import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq
my_key=os.environ.get('SECRET_KEY')
client= Groq(api_key=my_key)

def script(role,key):
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{'role': 'system','content': role},
                  {'role': 'user', 'content': key}
                  ]
    )
    return response.choices[0].message.content

def extract_point(text):
    response='you are a business analyst, with years of experience, make analysis of a business'
    return script(response,text) 

def bulletpoints(key_points):
    role='summarize analysis in key points'
    return script(role,key_points)


if __name__ == "__main__":
    user_input=input("Question:" )
    step1output=extract_point(user_input)
    print("\n--- Step 1: Key Points Extracted ---")
    print(step1output)

    step2output=bulletpoints(step1output)
    print("\n--- Step 2: bullet Points Extracted ---")
    print(step2output)
     
