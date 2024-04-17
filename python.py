
from aljazeera.driver import AljazeeraDriver


aljazeera_driver:AljazeeraDriver = AljazeeraDriver()

aljazeera_driver.run_process(search_phrase='united', number_of_months=0 ,news_category="sections") #valid
# aljazeera_driver.run_process(search_phrase='media', number_of_months=0 ,news_category="sections") #valid
# aljazeera_driver.run_process(search_phrase='asdamsdasdlnasdjlajsd', number_of_months=0 ,news_category="sections") #invalid input