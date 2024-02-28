import nltk, string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_doc(doc):
    sentence_tokens = []
    
    # Clean text    
    doc = re.sub(r'\s+', ' ', doc)  # Replace multiple spaces with a single space
    #print(doc + "\n")
    
    doc = re.sub(r'http\S+', '', doc)  # Remove URLs
    #print(doc + "\n")
    
    # Split text into sentences
    sentences = nltk.sent_tokenize(doc)
    for sentence in sentences:
        sentence_tokens.append(preprocess_sentence(sentence))

    return '\n'.join(sentence_tokens)

def preprocess_sentence(sentence):
    
    # Tokenize & Normalize
    tokens = [word.lower() for word in word_tokenize(sentence)]
    #print(tokens)
    #print("\n")
    
    stop_words = set(stopwords.words('english'))
    remove_stopword(stop_words, "here")
  
    # Filter stopwords
    tokens = [word for word in tokens if word not in stop_words and not word.startswith("'") and word not in string.punctuation]    
    #print(tokens)
    #print("\n")
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    #print(tokens)
    #print("\n")
    
    # Alternatively, for Stemming
    # from nltk.stem.porter import PorterStemmer
    # stemmer = PorterStemmer()
    # tokens = [stemmer.stem(word) for word in tokens]

    return ' '.join(tokens)

def add_stopword(stop_words, word):
    # Add the word and its case variations
    for variant in {word.lower(), word.upper(), word.title()}:
        if variant not in stop_words: stop_words.add(variant)
        
def remove_stopword(stop_words, word):
    # Remove the word and its case variations
    for variant in {word.lower(), word.upper(), word.title()}:
        if variant in stop_words: stop_words.discard(variant)


            
# Example usage
#sample_text = "Here's an example sentence: preprocessing texts can be fun!"
#preprocessed_text = preprocess(sample_text)
#print(preprocessed_text)


