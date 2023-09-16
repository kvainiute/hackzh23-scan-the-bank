from transformers import pipeline
import re

ner = pipeline("ner",
               aggregation_strategy="simple",
               model= "models/bert-base-NER",
               tokenizer = "models/bert-base-NER")
def checkNer(resNer):
    for item in resNer:
        print(item)
        if item['entity_group'] == 'PER' and item['score'] > 0.5 and len(item['word']) > 7:
            return True
        if item['entity_group'] == 'ORG' and item['score'] > 0.9:
            return True
    return False

def classify(file_content):
    #
    # direct sensitive data
    #

    if file_content == '':
        return False

    # RSA private key
    hasRSA = file_content.find('-----BEGIN RSA PRIVATE KEY-----') != -1
    if hasRSA:
        return True
    
    # email regex
    email_regex = r"[\w\.-]+@[\w\.-]+"
    isDirect = bool(re.search(email_regex, file_content))

    # full name and company NER

    if not isDirect:
        resNer = ner(file_content)
        return checkNer(resNer)

    
    # IBAN regex
    iban_regex = r"[A-Z]{2}[0-9]{2}(?:[ ]?[0-9]{4}){4}(?!(?:[ ]?[0-9]){3})(?:[ ]?[0-9]{1,2})"
    isIndirect = bool(re.search(iban_regex, file_content))

    if not isIndirect:
        # Phone number regex
        phone_number_regex = r"[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}"
        isIndirect = bool(re.search(phone_number_regex, file_content))

    return isDirect and isIndirect
