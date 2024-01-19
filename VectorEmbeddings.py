from transformers import BertTokenizer, BertModel
import torch

# Load pre-trained model tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def encode_text(text):
    # Tokenize and encode the text
    encoded = tokenizer.encode_plus(
        text,
        add_special_tokens=True,  # Add '[CLS]' and '[SEP]'
        return_attention_mask=True,
        padding='max_length',  # Pad to a max length
        truncation=True,
        max_length=512,  # Max length to truncate/pad
        return_tensors='pt',  # Return PyTorch tensors
    )
    return encoded['input_ids'], encoded['attention_mask']

def create_embeddings(input_ids, attention_mask):
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        embeddings = outputs.last_hidden_state
        return embeddings
    
# Example usage
text = "Example sentence for encoding"
input_ids, attention_mask = encode_text(text)
embeddings = create_embeddings(input_ids, attention_mask)


# Get the embeddings of the '[CLS]' token (for sentence-level embeddings)
sentence_embedding = embeddings[0, 0]

print(sentence_embedding)
