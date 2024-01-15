import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess(text):
    # Clean text
    text = re.sub(r'\W+', ' ', text)  # Remove all non-word characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    
    # Tokenize & Normalize
    tokens = [word.lower() for word in word_tokenize(text)]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Alternatively, for Stemming
    # from nltk.stem.porter import PorterStemmer
    # stemmer = PorterStemmer()
    # tokens = [stemmer.stem(word) for word in tokens]

    return ' '.join(tokens)

# Example usage
sample_text = "Here's an example sentence: preprocessing texts can be fun!"
preprocessed_text = preprocess(sample_text)
print(preprocessed_text)


