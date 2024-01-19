import spacy, platform
import re

if platform.system() == "Windows": pass

if platform.system() == "Linux": pass

def preprocess_doc(doc, lang):
    spacy.prefer_gpu()
    
    # Load English or German model for tokenization and preprocessing
    nlp = spacy.load("en_core_web_sm")
    if lang == 'german': nlp = spacy.load("de_core_news_sm")
    
    # Clean text    
    doc = re.sub(r'\s+', ' ', doc)  # Replace multiple spaces with a single space
    print(doc + "\n")
    
    doc = re.sub(r'http\S+', '', doc)  # Remove URLs
    print(doc + "\n")
    
    # Process the document
    doc = nlp(doc)
    sentence_tokens = []
    sentences = [sentence.text for sentence in doc.sents]
    
    # Iterate through the sentences
    for sentence in sentences:
        sentence_tokens.append(preprocess_sentence(sentence, nlp))
            
    return '\n'.join(sentence_tokens)

def preprocess_sentence(sentence, nlp_model):    
    remove_stopword(nlp_model, "Here")
    
    # Process text using spaCy
    sentence = nlp_model(sentence)
    
    # Tokenization and Lemmatization with spaCy (and normalization (lowercasing))
    tokens = [token.lemma_.lower() for token in sentence if not token.is_stop and not token.is_punct]

    return ' '.join(tokens)

def add_stopword(pipeline, word):
    # Add the word and its case variations
    for variant in {word.lower(), word.upper(), word.title()}:
        pipeline.Defaults.stop_words.add(variant)
        pipeline.vocab[variant].is_stop = True

def remove_stopword(pipeline, word):
    # Remove the word and its case variations
    for variant in {word.lower(), word.upper(), word.title()}:
        if variant in pipeline.Defaults.stop_words:
            print("variant: " + variant + "\n")
            pipeline.Defaults.stop_words.remove(variant)
            pipeline.vocab[variant].is_stop = False
            
# Example usage
#sample_text = "Here's an example sentence: preprocessing texts can be fun!"
#preprocessed_text = preprocess(sample_text)
#print(preprocessed_text)
