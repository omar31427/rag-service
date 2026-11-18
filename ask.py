from dotenv import load_dotenv
load_dotenv()
from retrieval import embed, load_dotenv, search, connect, client

COURSE_ID = 2

def build_context(rows):
    parts = []
    for number, (source, page, content, score) in enumerate(rows, start=1):
        first_line = f"[{number}] (source: {source}, page: {page})"
        part = first_line + "\n" + content
        parts.append(part)
    return "\n\n".join(parts)




with connect() as conn:

    while True:
        question = input("Question: ")
        embedded_question = embed(question)
        
        rows = search(conn, embedded_question, COURSE_ID, k=8)

        if not rows or rows[0][3] < 0.2:
            print(f"i dont know")
            continue

        context = build_context(rows)

        response = client.chat.completions.create(
            model="gpt-6-luna",
            messages=[
                {"role": "system", "content": """
                    You are a teaching assistant for a university course.
                    Answer the student's question using ONLY the course material provided.
                    If the answer is not in the material, say you don't know and suggest asking the lecturer or the course forum.
                    If the material contains a closely related rule the student should know about, mention it briefly.
                    Do not use outside knowledge, even if you know the answer.
                    Answer in the same language as the question.
                    Keep answers short and clear.
                    After each fact, cite its source number in brackets, like [1].
                    """
                },
                {"role": "user", "content": f"Course material:\n{context}\n\nQuestion: {question}"},
            ],
        )

        answer = response.choices[0].message.content
        print(answer)
        
        for number, (source, page, content, score) in enumerate(rows, start=1):
            print(f"[{number}] {source}, page {page}")
            print(f"#######################################################3")
            print(f"#######################################################3")

        usage = response.usage
        print(f"input tokens: {usage.prompt_tokens}\n")
        print(f"output tokens: {usage.completion_tokens}\n")
        cost = usage.prompt_tokens * 0.10 / 1_000_000 + usage.completion_tokens * 0.50 / 1_000_000
        print(f"cost: {cost}\n")

        break_question = input("would you like to continue?")
        if break_question == "n" or break_question == "N":
            break

