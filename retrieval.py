import psycopg
from pgvector.psycopg import register_vector
from dotenv import load_dotenv
from openai import OpenAI
import os
import numpy as np

load_dotenv()
client = OpenAI()

def connect():
    conn = psycopg.connect(host="localhost", port=5433, dbname="rag",
                           user="rag", password=os.getenv("POSTGRES_PASSWORD"))
    register_vector(conn)
    return conn
    
def embed(text):
    response = client.embeddings.create(model="text-embedding-3-small", input = text)
    vector = np.array(response.data[0].embedding)

    return vector

def search(conn, vector, course_id, k=3):
    cur = conn.execute (
            """SELECT source, page, content, 1 - (embedding <=> %s) AS score
            FROM chunks
            WHERE course_id = %s
            ORDER BY embedding <=> %s
            LIMIT %s
            """ 
            , (vector, course_id, vector, k)
        )
    return cur.fetchall()
