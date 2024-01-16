import nltk_sentence_prep as nl
import re

def preprocess_text(text):
    sentence_tokens = []
    
    # Clean text    
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    print(text + "\n")
    
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    print(text + "\n")
    
    # Split text into sentences
    sentences = nl.nltk.sent_tokenize(text)
    for sentence in sentences:
        sentence_tokens.append(nl.preprocess(sentence))

    return '\n'.join(sentence_tokens)