from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-6-luna",
    messages=[
        {"role": "system", "content": """
            You are a teaching assistant for a university course.
            Answer the student's question using ONLY the course material provided.
            If the answer is not in the material, say you don't know and suggest asking the lecturer or the course forum.
            Do not use outside knowledge, even if you know the answer.
            Answer in the same language as the question.
            Keep answers short and clear.
            After each fact, cite its source number in brackets, like [1].
            """
        },
        {"role": "user", "content": f"Course material: {context}, Question: {question}"},
    ],
)

print(response.choices[0].message.content)
print(response.usage)

