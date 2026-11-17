from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
response = client.embeddings.create(model="text-embedding-3-small", input="your sentence")
vector = response.data[0].embedding
print(f"len res: {len(vector)}, \n vector: {vector[:5]}")
