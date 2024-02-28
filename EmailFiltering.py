from genericpath import isdir
import extract_msg, os
from langdetect import detect
import hashlib, re
import spacy_sentence_preprocess as ssp

# Filter duplicate emails via hashing of the email content
def get_hash(email_body):
    return hashlib.sha256(email_body.encode()).hexdigest()

def email_body(filename):
    msg = extract_msg.Message(filename)
    body = msg.body
    
    # Define patterns for common email headers, footers, and greetings
    greeting_pattern = r"Dear .*,?\n|H[ea]llo(.*)?\n|Hi(.*)?,?\n"
    footer_pattern = (r"[Rr]egards(.*)?\n|[Ss]incerely(.*)\n|Best(.*)?\n|Thank you(.*)?\n|Thanks(.*)?\n|(.*)?[Ff]reundlich(.*)?\n|"
                      r"Beste Gr(.*)\n|[Vv]iele Gr(.*)\n|(.*)?Dank(e)?(,)?\n|Gru(.)(,)?\n|Gr(...)(,)?\n|[LBF]G(,)?\n" 
    )
    pattern_for_multiple_messages = f"({footer_pattern})(.*)?({greeting_pattern})"
    pattern_for_single_messages = f"({footer_pattern})(.*)?"
    
    # Remove headers, footers, and greetings
    body = re.sub(pattern_for_multiple_messages, '', body, flags=re.MULTILINE | re.DOTALL | re.UNICODE)
    body = re.sub(greeting_pattern, '', body, flags=re.MULTILINE | re.IGNORECASE | re.UNICODE)
    body = re.sub(pattern_for_single_messages, '', body, flags=re.MULTILINE | re.DOTALL | re.UNICODE)

    return body.strip()

def filter_emails(directory):
    title_filters = ["automatische antwort", "automatic reply", "abwesend_"] # emails to remove
    hashes = []
    unique_texts = []
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
     
        for filename in os.listdir(subdir_path):
            redundant_email = False
            for term in title_filters:
                if term in filename.lower():
                    redundant_email = True
                    break
               
            # Construct absolute file path and check if it's a file and not a directory
            if not redundant_email and filename.endswith(".msg"):
                file_path = os.path.join(subdir_path, filename)
           
                try:
                    body = email_body(file_path)
                    hash_val = get_hash(body)
                    if hash_val not in hashes: 
                        hashes.append(hash_val)
                        if detect(body) == 'de': 
                            doc = ssp.preprocess_doc(body, "german")
                            unique_texts.append([doc, 'German', file_path])
                            print(doc)
                            print("/n")
                        elif detect(body) == 'en': 
                            doc = ssp.preprocess_doc(body)
                            print(doc)
                            print("/n")
                            unique_texts.append([doc, 'English', file_path])
                                     
                except: continue
                
            # preprocessing all emails take too much time, hence the code is tried with only 100 of them    
            if len(unique_texts) == 100:  
                return unique_texts
    