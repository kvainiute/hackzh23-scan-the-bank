from transformers import pipeline
import re

#question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')
ner = pipeline("ner", aggregation_strategy="simple")

def checkNer(resNer):
    for item in resNer:
        if item['entity_group'] == 'PER':
            return True
        if item['entity_group'] == 'ORG':
            return True
    return False

def classify(file_content):
    #
    # direct sensitive data
    #
    
    # RSA private key
    hasRSA = file_content.find('-----BEGIN RSA PRIVATE KEY-----') != -1
    if hasRSA:
        return True
    
    # email regex
    email_regex = r"[\w\.-]+@[\w\.-]+"
    hasEmail = bool(re.search(email_regex, file_content))
    
    # IBAN regex
    iban_regex = r"[A-Z]{2}[0-9]{2}(?:[ ]?[0-9]{4}){4}(?!(?:[ ]?[0-9]){3})(?:[ ]?[0-9]{1,2})"
    hasIBAN = bool(re.search(iban_regex, file_content))
    if hasIBAN and hasEmail:
        return True

    # return "review"


    # full name NER

    resNer = ner(file_content)
    return checkNer(resNer)





    # full name
    fullName = question_answerer(
        question = "What is the person's full name?",
        context = file_content
    )
    hasFullName = fullName['score'] > 0.5
    return hasFullName or hasEmail

    model_name = "bert-base-uncased"
    model = BertForTokenClassification.from_pretrained(model_name)
    tokenizer = BertTokenizer.from_pretrained(model_name)

    tokenized_text = tokenizer.tokenize(file_content)

    inputs = tokenizer(tokenized_text, padding=True, truncation=True, return_tensors="pt")
    outputs = model(**inputs)

    logits = outputs.logits
    predictions = torch.argmax(logits, dim=2)