from pypdf import PdfReader


def chunk_text(text, size=900, overlap=150):
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")

    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        if end < len(text):
            last_space = text.rfind(" ", start, end)
            if last_space > start:
                end = last_space

        chunks.append(text[start : end].strip())
        if start + size >= len(text):   # this chunk reached the end of the text
            break
        
        position = max(end - overlap, start + 1)    # never look back before this chunk
        new_start = text.find(" ", position) + 1    # +1 = first letter after the space
        if new_start <= start or new_start > end:   # didn't move forward, or jumped too far
            new_start = end
        
        start = new_start

    return chunks

def make_chunk_dicts(source, page, chunks):
    dictated_chunks = []
    for chunk in chunks:
        dictated_chunks.append({
            "source": source,
            "page": page+1,
            "text": chunk
        })
    return dictated_chunks

def get_chunks_in_dicts(path):
    reader = PdfReader(path)

    chunks_in_dicts = []
    for index,page in enumerate(reader.pages):
        clean_page = " ".join(page.extract_text().split())

        chunks = chunk_text(clean_page, size=900, overlap=150)

        chunks_in_dicts.extend(make_chunk_dicts(path.name,index,chunks))

    return chunks_in_dicts

if __name__ == "__main__":

    path = 'data/ch_loops.pdf'

    chunks_in_dicts = get_chunks_in_dicts(path)
    print(f"len ordered_chunkxs chunks: {len(chunks_in_dicts)}")
    for i in range (0,3):
        print(f"chunk {i}: {chunks_in_dicts[i]}")



