import numpy as np

def cosine_similarity(A, B):
    
    if(len(A) != len(B)):
        raise ValueError("Vectors must be of the same length")
    
    vect_sum = sum(a * b for a, b in zip(A, B))
    magnitude_A = np.sqrt(sum(a ** 2 for a in A))
    mabgitude_B = np.sqrt(sum(b ** 2 for b in B))

    if magnitude_A == 0 or mabgitude_B == 0:
        raise ValueError("Vectors must not be zero vectors")
    
    return vect_sum / (magnitude_A * mabgitude_B)
    

def top_k_similar(query_vector, document_vectors, k):
    similarities = [cosine_similarity(query_vector, doc_vector) for doc_vector in document_vectors]
    top_k_indices = np.argsort(similarities)[-k:][::-1]
    return top_k_indices, [similarities[i] for i in top_k_indices]

def main():
    query_vector = [1, 0, 0]
    document_vectors = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 0],
        [1, 0, 1]
    ]
    
    top_k_indices, top_k_similarities = top_k_similar(query_vector, document_vectors, k=3)
    
    print("Top K Similar Indices:", top_k_indices)
    print("Top K Similarities:", top_k_similarities)

if __name__ == "__main__":
    main()