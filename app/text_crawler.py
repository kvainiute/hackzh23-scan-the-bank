from transformers import pipeline
import re

ner = pipeline("ner",
               aggregation_strategy="simple",
               model="/models/bert-base-NER",
               tokenizer="/models/bert-base-NER")

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
    is_direct = bool(re.search(email_regex, file_content))

    # full name and company NER
    is_indirect = False
    if not is_direct:
        resNer = ner(file_content)
        for item in resNer:
            if item['entity_group'] == 'PER' and item['score'] > 0.5 and len(item['word']) > 7:
                is_direct = True
            if item['entity_group'] == 'ORG' and item['score'] > 0.9:
                is_direct = True
            if item['entity_group'] == 'LOC' and item['score'] > 0.9:
                is_indirect = True

    
    # IBAN regex
    iban_regex = r"[A-Z]{2}[0-9]{2}(?:[ ]?[0-9]{4}){4}(?!(?:[ ]?[0-9]){3})(?:[ ]?[0-9]{1,2})"
    is_indirect = bool(re.search(iban_regex, file_content))

    if not is_indirect:
        # Phone number regex
        phone_number_regex = r"[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}"
        is_indirect = bool(re.search(phone_number_regex, file_content))

    return is_direct or is_indirect
