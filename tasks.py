from robocorp.tasks import task
from robocorp import workitems

from selenium_flow.aljazeera import constant as aljazeera_constants
from selenium_flow.aljazeera.driver import AljazeeraDriver 

from exceptions import SearchPhraseEmptyException, NumberOfMonthsEmptyException,NumberOfMonthsInvalidTypeException , NumberOfMonthsInvalidValueTypeException

@task 
def run_aljazeera_news_pull():
    """ Pull articles from the Aljazeera news site"""

    aljazeera_driver:AljazeeraDriver = AljazeeraDriver()

    payload:dict = workitems.inputs.current.payload
    search_phrase = payload.get("search_phrase")
    number_of_months = payload.get("number_of_months",0)
    validate_search_phrase(search_phrase)
    validate_number_of_months(number_of_months)
    
    aljazeera_driver.run_process(search_phrase=search_phrase, number_of_months=number_of_months,) #valid


def validate_search_phrase(search_phrase):
    """ 
    raise Exception if search_phrase is empty
    """
    if not search_phrase:
        raise SearchPhraseEmptyException(search_phrase=search_phrase) 
    

def validate_number_of_months(number_of_months):
    """ 
    raise Exceptions if number_of_months is empty or invalid
    """
    if number_of_months is None:
        raise NumberOfMonthsEmptyException(number_of_months=number_of_months) 
    if not isinstance(number_of_months,int):
        raise NumberOfMonthsInvalidTypeException(number_of_months=number_of_months)
    if number_of_months < 0:
        raise NumberOfMonthsInvalidValueTypeException(number_of_months=number_of_months)
    
    