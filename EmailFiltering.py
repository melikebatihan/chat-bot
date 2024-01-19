import extract_msg
from langdetect import detect
import hashlib

# Filter duplicate emails via hashing of the email content
def filter_duplicates(email):
    return hashlib.sha256(email.encode()).hexdigest()

def detect_language(text):
    try:
        return detect(text)
    except:
        return None  # In case of detection error

# Example usage
text = "This is a sample text."
language = detect_language(text)
print(language)  # Outputs 'en' for English, 'de' for German, etc.

def email_body(filename):
    msg = extract_msg.Message(filename)
    body = msg.body
    # Further processing can be done here
    return body

# Example usage
body = email_body('path_to_msg_file.msg')

