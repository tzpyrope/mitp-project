from .dates_conversion.instruct_and_date_conversion import *
from .mode2 import *


def get_class_type_and_subject_name():
    pass
    # (class_type, subject, irrelevant) = type_and_subject

    # return class_type, subject
    
    
def test():
    tuple_test = get_class_type_and_subject_name()
    (class_type, subject) = tuple_test

    return f"{subject}, {class_type}"
