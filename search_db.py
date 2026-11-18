import psycopg
from pgvector.psycopg import register_vector
from dotenv import load_dotenv
from openai import OpenAI
import os
import numpy as np

load_dotenv()
client = OpenAI()
COURSE_ID = 2

with psycopg.connect(host="localhost", port=5433, dbname="rag",
    user="rag",password=os.getenv("POSTGRES_PASSWORD")) as conn:
    register_vector(conn)

    while True:
        question = input("Question: ")
        response = client.embeddings.create(model="text-embedding-3-small", input = question)
        embedded_question = np.array(response.data[0].embedding)
        cur = conn.execute (
            """SELECT source, page, content, 1 - (embedding <=> %s) AS score
            FROM chunks
            WHERE course_id = %s
            ORDER BY embedding <=> %s
            LIMIT 3
            """ 
            , (embedded_question, COURSE_ID, embedded_question)
        )
        rows = cur.fetchall()

        if not rows or rows[0][3] < 0.2:
            print(f"i dont know")
            continue

        for index in range(3):
            print(f"source: {rows[index][0]}")
            print(f"page: {rows[index][1]}")
            print(f"text: {rows[index][2][:150]}")
            print(f"score: {rows[index][3]}")
            print(f"#######################################################3")
            print(f"#######################################################3")

        

        break_question = input("would you like to continue?")
        if break_question == "n" or break_question == "N":
            break
