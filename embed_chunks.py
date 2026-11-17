from chunking import  get_chunks_in_dicts, chunk_text, make_chunk_dicts
from pathlib import Path
from pypdf import PdfReader
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

syllabus = Path("data/syllabus.txt").read_text(encoding="utf-8")
syllabus = " ".join(syllabus.split())
syllabus_chunks = chunk_text(syllabus, size=900, overlap=150)
syllabus_chunks_in_dicts = make_chunk_dicts("syllabus.txt", 0, syllabus_chunks)

file_paths = sorted(Path("data").glob("*.pdf"))

chunks = []
chunks.extend(syllabus_chunks_in_dicts)
for fp in file_paths:
    chunks.extend(get_chunks_in_dicts(fp))

print(f"len chunks: {len(chunks)}")

start = 0
len_chunks = len(chunks)
total_tokens = 0
while start < len_chunks:
    batch = chunks[start : start + 100]
    batch_texts = [c["text"] for c in batch]

    end = start + 100
    response = client.embeddings.create(model="text-embedding-3-small", input = batch_texts)
    total_tokens += response.usage.total_tokens
    vectors = response.data
    for index,v in enumerate(vectors):
        chunks[start + index]["embedding"] = v.embedding

    start += 100


with open("chunks.json", "w", encoding="utf-8") as file:
    json.dump(chunks,file,ensure_ascii=False)



print(f"number of chunks embedded: {len(chunks)}")
print(f"number of tokens used: {total_tokens}")