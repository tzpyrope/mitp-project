from .instruct_and_date_conversion import *
from .mode2 import *

class Mode5(Mode2):
    def get_class_type_and_subject_name(self):
        type_and_subject = super(Mode5, self).get_class_type_and_subject_name()
        (class_type, subject, class_type_str) = type_and_subject

        return class_type, subject
    
    
    def __str__(self):
        tuple_test = self.get_class_type_and_subject_name()
        (class_type, subject) = tuple_test

        return f"{subject}, {class_type}"