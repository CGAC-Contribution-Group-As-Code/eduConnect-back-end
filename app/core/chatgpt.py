import openai
import os

def ask_ai(prompt, template):
    openai.api_key = os.getenv("CHATGPT_KEY")
    # completion = openai.Completion.create(
    # engine='text-davinci-003'  # 'text-curie-001'  # 'text-babbage-001' #'text-ada-001'
    # , prompt=prompt
    # , temperature=0.5
    # , max_tokens=1024
    # , top_p=1
    # , frequency_penalty=0
    # , presence_penalty=0)
    # return completion['choices'][0]['text']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": template
            },
            {
            "role": "user",
            "content":prompt
            },
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]["message"]['content']