import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
def dot(a,b):
    multiples = []
    for first,second in zip(a,b):
        multiples.append(first*second)

    return sum(multiples)

chunks = []
with open("chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)


while True:
    question = input("Question: ")
    response = client.embeddings.create(model="text-embedding-3-small", input = question)
    embedded_question = response.data[0].embedding
    for chunk in chunks:
        chunk["score"] = dot(chunk["embedding"],embedded_question)

    sorted_chunks = sorted(chunks, key = lambda c: c["score"], reverse = True)

    if sorted_chunks[0]["score"] < 0.2:
        print(f"i dont know")
        continue

    for index in range(3):
        print(f"source: {sorted_chunks[index]["source"]}")
        print(f"page: {sorted_chunks[index]["page"]}")
        print(f"text: {sorted_chunks[index]["text"][:150]}")
        print(f"score: {sorted_chunks[index]["score"]}")
        print(f"#######################################################3")
        print(f"#######################################################3")

    

    break_question = input("would you like to continue?")
    if break_question == "n" or break_question == "N":
        break

    
    