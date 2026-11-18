import os
import json
import numpy as np
import psycopg
from pgvector.psycopg import register_vector
from dotenv import load_dotenv

load_dotenv()
COURSE_ID = 2

with open("chunks.json","r", encoding="utf-8") as file:
    chunks = json.load(file)

with psycopg.connect(host="localhost", port=5433, dbname="rag",
                     user="rag", password=os.getenv("POSTGRES_PASSWORD")) as conn:
    register_vector(conn)

    conn.execute(
        "DELETE FROM chunks WHERE course_id = %s", (COURSE_ID,)
        )
 
    for chunk in chunks:
        conn.execute(
            "INSERT INTO chunks(course_id, source, page, content, embedding) VALUES (%s, %s, %s, %s, %s)",
            (COURSE_ID, chunk["source"], chunk["page"], chunk["text"],np.array(chunk["embedding"]))
        )
print(f"inserted {len(chunks)} chunks")