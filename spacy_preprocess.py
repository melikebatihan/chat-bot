import spacy, platform
import re

if platform.system() == "Windows": pass

if platform.system() == "Linux": pass

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    # Clean text
    text = re.sub(r'\W+', ' ', text)  # Remove all non-word characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    
    # Process text using spaCy
    doc = nlp(text)

    # Tokenization and Lemmatization with spaCy
    # Additionally, spaCy takes care of normalization (lowercasing)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]

    return ' '.join(tokens)

# Example usage
sample_text = "Here's an example sentence: preprocessing texts can be fun!"
preprocessed_text = preprocess(sample_text)
print(preprocessed_text)
