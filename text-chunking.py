def chunking(text, chunk_size=250, overlap=50):
    """
    Splits the input text into chunks of specified size with optional overlap.

    Parameters:
    text (str): The input text to be chunked.
    chunk_size (int): The size of each chunk in characters. Default is 250.
    overlap (int): The number of characters to overlap between chunks. Default is 50.

    Returns:
    list: A list of text chunks.
    """
    if chunk_size <= 0 or overlap < 0:
        raise ValueError("Chunk size and overlap must be positive integers.")
    
    start = 0
    chunks = []
    words = text.split()

    while start < len(text):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def main():
    text = "This is an example of a long text that needs to be chunked into smaller pieces for processing. "
    text += "The chunking function will help in breaking down the text into manageable parts, especially when dealing with large documents."
    text += " Each chunk will have a specified size and can overlap with the next chunk to ensure that important context is not lost."
    text += " This is particularly useful in natural language processing tasks where the context of words is crucial for understanding."
    text += " By using the chunking function, we can efficiently process large texts without running into memory issues or losing important information."
    chunks = chunking(text, chunk_size=50, overlap=10)
    print("Chunks:")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk}")

if __name__ == "__main__":
    main()  