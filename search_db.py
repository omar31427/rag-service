import psycopg
from pgvector.psycopg import register_vector
from dotenv import load_dotenv
from openai import OpenAI
import os
import numpy as np
from retrieval import embed, load_dotenv, search, connect

client = OpenAI()
COURSE_ID = 2

with connect() as conn:
    register_vector(conn)

    while True:
        question = input("Question: ")
        embedded_question = embed(question)
        
        rows = search(conn, embedded_question, COURSE_ID, k=3)

        if not rows or rows[0][3] < 0.2:
            print(f"i dont know")
            continue

        for source, page, content, score in rows:
            print(f"source: {source}")
            print(f"page: {page}")
            print(f"text: {content[:150]}")
            print(f"score: {score}")
            print(f"#######################################################3")
            print(f"#######################################################3")

        

        break_question = input("would you like to continue?")
        if break_question == "n" or break_question == "N":
            break
