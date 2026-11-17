from pypdf import PdfReader
path = 'data/ch_loops.pdf'
reader = PdfReader(path)
print(f"len pages: {len(reader.pages)}")
print(f"page 0: {reader.pages[0].extract_text()}")
clean = " ".join(reader.pages[0].extract_text().split())
print(f"len clean: {len(clean)}")