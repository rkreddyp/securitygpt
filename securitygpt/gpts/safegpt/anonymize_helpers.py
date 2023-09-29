
from presidio_analyzer import Pattern, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine
from presidio_analyzer import AnalyzerEngine

from presidio_anonymizer.entities import (
    RecognizerResult,
    OperatorResult,
    OperatorConfig,
)

def get_recognizer_and_entities():

    numbers_pattern = Pattern(name="numbers_pattern", regex="\d+", score=0.5)
    number_recognizer = PatternRecognizer( supported_entity="NUMBER", patterns=[numbers_pattern])
    ip_pattern = Pattern(name="ip_pattern", regex="\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b", score=0.5)
    ip_recognizer = PatternRecognizer( supported_entity="IP_ADDRESS", patterns=[ip_pattern])
    ec2_pattern = Pattern(name="ip_pattern", regex="\\b(i-[a-zA-Z0-9]+)\\b", score=0.5)
    ec2_recognizer = PatternRecognizer( supported_entity="EC2_ADDRESS", patterns=[ip_pattern])

    subnet_pattern = Pattern(name="subnet_pattern", regex="\\b(subnet-[a-zA-Z0-9]+)\\b", score=0.5)
    subnet_recognizer = PatternRecognizer( supported_entity="SUBNET_ADDRESS", patterns=[subnet_pattern])


    arn_pattern = Pattern(name="arn_pattern", regex="\\b(arn:[:]+:[:]+:[:]+:([0-9]))\\b", score=0.5)
    arn_recognizer = PatternRecognizer( supported_entity="ARN", patterns=[ip_pattern])
    ec2_or_number_pattern= Pattern(name="ec2_or_number_pattern", regex="\d+|\\b(?:\\d{1,3}\\.){3}\\d{1,3}+\\b\\b", score=0.5)
    ec2_or_number_recognizer = PatternRecognizer( supported_entity="EC2_ADDRESS_OR_NUMBER", patterns=[ec2_or_number_pattern])


    service_pattern = Pattern(name="service_pattern", regex="\\b(arn:[^:]+:([a-zA-Z0-9-]+):[^:]+:([0-9]{12}):[^:]+)\\b", score=0.5)
    service_recognizer = PatternRecognizer( supported_entity="AWS_SERVICE", patterns=[ip_pattern])

    email_pattern = Pattern(name="email_pattern", regex="\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\\b", score=0.5)
    email_recognizer = PatternRecognizer( supported_entity="EMAIL", patterns=[email_pattern])
    security_recognizer = PatternRecognizer( supported_entity="SECURITY", patterns=[ip_pattern, ec2_pattern, numbers_pattern, ec2_or_number_pattern, service_pattern, email_pattern, subnet_pattern])
    entities = ["IP_ADDRESS", "NUMBER", "EC2_ADDRESS", "ARN", "EC2_ADDRESS_OR_NUMBER", "AWS_SERVICE", "EMAIL", "SUBNET_ADDRESS"]

    return (security_recognizer, entities)