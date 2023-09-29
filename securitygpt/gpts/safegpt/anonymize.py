from .anonymize_helpers import get_recognizer_and_entities
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer import Pattern, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine
from presidio_anonymizer.entities import (
    RecognizerResult,
    OperatorResult,
    OperatorConfig,
)
import pandas as pd


def analyze (text, recognizer, entities):
    print ('recognize')
    analyzer = AnalyzerEngine()
    analyzer_result = recognizer.analyze(text=text, entities=entities)
    return analyzer_result


def encrypt (text):
    print ('anonymize')
    crypto_key = "WmZq4t7w!z%C&F)J"
    (recognizer, entities) =  get_recognizer_and_entities()
    analyzer_results = analyze(text, recognizer, entities)
    engine = AnonymizerEngine()
    anonymize_result = engine.anonymize(
        text=text,
        analyzer_results=analyzer_results,
        operators={"SECURITY": OperatorConfig("encrypt", {"key": crypto_key})},
    )
    return anonymize_result, analyzer_results

def decrypt_dataframe (text, dataframe):
    mapping_dict = dict(zip(dataframe['encrypted_string'], dataframe['plain_string']))

    decrypted_text = text
    for encrypted, plain in mapping_dict.items():
        decrypted_text = decrypted_text.replace(encrypted, plain)

    return decrypted_text

def decrypt(plain_text , analyzer_results, anonymizer_result):
    plain_list = []
    encrypted_list = []
    for result in analyzer_results:
        print(result.entity_type, result.start, result.end, plain_text[result.start:result.end])
        plain_list.append(plain_text[result.start:result.end])

    encrypted_text = anonymizer_result.text
    anonymized_entities = anonymizer_result.items
    #anon_df = pd.DataFrame(anonymizer_result.items)
    sorted_data = sorted(anonymizer_result.items, key=lambda x: x.start, reverse=False)
        
    # Create an ordered list from the sorted data
    ordered_list = sorted_data
    anonymized_entities = ordered_list
    print (encrypted_text)
    for results in anonymized_entities :
        print (results)
        encrypted_list.append(anonymizer_result.text[results.start:results.end])

    print (len(plain_list), len(encrypted_list))
    df = pd.DataFrame({'plain_string': plain_list, 'encrypted_string': encrypted_list})
    
    decrypted_text = decrypt_dataframe(encrypted_text, df)
    return decrypted_text

def get_mappings ( plain_text , analyzer_results, anonymizer_result):
    plain_list = []
    encrypted_list = []
    for result in analyzer_results:
        print(result.entity_type, result.start, result.end, plain_text[result.start:result.end])
        plain_list.append(plain_text[result.start:result.end])

    encrypted_text = anonymizer_result.text
    anonymized_entities = anonymizer_result.items
    #anon_df = pd.DataFrame(anonymizer_result.items)
    sorted_data = sorted(anonymizer_result.items, key=lambda x: x.start, reverse=False)
        
    # Create an ordered list from the sorted data
    ordered_list = sorted_data
    anonymized_entities = ordered_list
    print (encrypted_text)
    for results in anonymized_entities :
        print (results)
        encrypted_list.append(anonymizer_result.text[results.start:results.end])

    print (len(plain_list), len(encrypted_list))
    df = pd.DataFrame({'plain_string': plain_list, 'encrypted_string': encrypted_list})
    return df