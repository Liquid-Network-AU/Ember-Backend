import spacy

# Load the pre-trained English language model
nlp = spacy.load("en_core_web_sm")

# Define a function that takes a string and returns a list of its word embeddings
def get_embeddings(text):
    # Process the text with spaCy
    doc = nlp(text)

    # Return the average of the word vectors in the document
    return doc.vector.tolist()

# Example usage
text = "The quick brown fox jumps over the lazy dog."
embeddings = get_embeddings(text)
print(embeddings)