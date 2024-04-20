from robocorp.tasks import task
from robocorp import workitems

from selenium_flow.aljazeera import constant as aljazeera_constants
from selenium_flow.aljazeera.driver import AljazeeraDriver 


@task 
def run_aljazeera_news_pull():
    """ Pull articles from the Aljazeera news site"""

    aljazeera_driver:AljazeeraDriver = AljazeeraDriver()

    payload:dict = workitems.inputs.current.payload
    print(payload, "checking_payload")
    search_phrase = payload.get("search_term")
    number_of_months = payload.get("number_of_months",0)
    search_phrase_is_valid:bool = validate_search_phrase(search_phrase)
    number_of_months_is_valid:bool = validate_number_of_months(number_of_months)
    if not search_phrase_is_valid:
        raise Exception("'search_phrase' is invalid|missing")
    if not number_of_months_is_valid:
        raise Exception("'number_of_months' is invalid")
    
    aljazeera_driver.run_process(search_phrase=search_phrase, number_of_months=number_of_months,) #valid


def validate_search_phrase(search_phrase):
    """ 
    returns True if search_phrase is not empty; returns False if search_phrase is empty
    """
    return not search_phrase

def validate_number_of_months(number_of_months):
    """ 
    returns True if number_of_months is greater than , or equal to 0. otherwise returns False
    """
    if number_of_months is None:
        return False 
    if not isinstance(number_of_months,int):
        return False 
    
    return number_of_months >= 0