
from datetime import date, datetime
import datetime
from time import sleep
from typing import Optional

import pandas as pd 

from selenium_flow.aljazeera.logger import logger
from selenium_flow.aljazeera import constant as aljazeera_constant
from selenium_flow.aljazeera.helper import extract_values_from_article_html, get_start_and_end_date_from_current_month, save_dataframe, validate_news_category,convert_to_table, save_table_as_xlsx
from selenium_flow.driver import BaseDriver

class AljazeeraDriver(BaseDriver):

    def __init__(self, window_width: Optional[int] = None, window_height: Optional[int] = None, disable_images: Optional[bool] = False) -> None:
        super().__init__(window_width, window_height, disable_images)
        logger.info("Initialized driver")
    
    def __del__(self):
        # driver auto closes
        ...
         

    def run_process(self, search_phrase:str, number_of_months:int, news_category:Optional[str]=None):
        """
        
        runs the whole extraction and formatting process

        Args:
            search_phrase (str): search phrase input 
            number_of_months (int): number of months for date filtering
            news_category (Optional[str]): news category (does not exist for Aljazeera)
        """
        results:list = []
        logger.info("calculating start and end dates")
        start_date_time, end_date_time = get_start_and_end_date_from_current_month(number_of_months=number_of_months)

        start_date_time:date
        end_date_time:date

        date_time_format:str = "%Y-%m-%d" 
        logger.info(f"Input parameter_Search Phrase --- {search_phrase}")
        logger.info(f"Input parameter_pulling news from {start_date_time.strftime(date_time_format)} to {end_date_time.strftime(date_time_format)}")

        logger.info("Navigating to Aljazeera Website ") 
        self.driver.open_available_browser(aljazeera_constant.WEBSITE_URL, headless=False, maximized=True,options='add_argument("--incognito")')
        logger.info("Navigated to website ")
        

        self.run_search_phrase(search_phrase)
        self.add_filters()
        results:list  = self.parse_results(search_phrase=search_phrase,start_date_time=start_date_time)

        logger.info("Converting result to RPA.Tables object")
        article_table = convert_to_table(result=results)

        logger.info(f"Saving results to fixtures path {aljazeera_constant.FIXTURES_PATH}")
        save_table_as_xlsx(article_table=article_table)




    def run_search_phrase(self, search_phrase):
        """
        
        inputs search phrase into input field and clicks on search

        Args:
            search_phrase (_type_): search phrase input
        """
        try:
            

            logger.info("Click search icon")
            search_icon_xpath:str = 'xpath:/html/body/div[1]/div/div[1]/div[1]/div/header/div[4]/div[2]/button'
            self.click_xpath(search_icon_xpath,15)
            

            logger.info(f"Inputing search phrase '{search_phrase}'")

            input_field_xpath:str = 'xpath://*[@id="root"]/div/div[1]/div[2]/div/div/form/div[1]/input'
            
            self.input_xpath(input_field_xpath, search_phrase)

            search_field_icon:str = 'xpath://*[@id="root"]/div/div[1]/div[2]/div/div/form/div[2]/button'
            logger.info("Clicking search icon")
            try:
                self.click_xpath(search_field_icon)
            except Exception as e:
                pass 
            

            logger.info("Search complete ....")
        except Exception as e:
            logger.error(f'Could not run query for {search_phrase} -- {e}')


    def add_filters(self):
        """
        
        sorts by 'Date' to show recent news article

        Args:
            category_list (set): _description_
        """
        try:
            logger.info("Sorting by Date")
            sort_by_dropdown_xpath:str ='xpath://*[@id="search-sort-option"]'
            self.click_xpath(sort_by_dropdown_xpath,200)

            newest_option_xpath:str = 'xpath://*[@id="search-sort-option"]/option[1]'
            self.click_xpath(newest_option_xpath)
        except Exception as e:
            logger.error(f'Could not add filters -- {e}')



    def parse_results(self, search_phrase:str, start_date_time:date):
        """
            iterates over news articles and formats them  
        """
        result:list  = [] 
        stop_parsing:bool = False
        count:int = 1

        while not stop_parsing:
            article_block_xpath:str = 'xpath://*[@id="main-content-area"]/div[2]/div[2]/article'
            self.driver.wait_until_element_is_visible(article_block_xpath,30)
            articles = self.driver.find_elements(article_block_xpath)
            logger.info(f"Found {len(articles)} articles")
            
            if count > len(articles):
                logger.info("Reached article size limit")
                break 

            # parse each item
            
            formatted_article:dict = self.format_article(count,search_phrase)
            # check date to know if parsing should stop
            last_extracted_date:str = formatted_article.get("date")
            if not last_extracted_date:
                raise Exception("Date not found")

            formatted_last_extracted_date = datetime.datetime.strptime(last_extracted_date,aljazeera_constant.DATE_FORMAT).date()

            # checks
            if formatted_last_extracted_date < start_date_time:
                stop_parsing = True 
                logger.info(f"{last_extracted_date} is lesser than start_date . Halt parsing ..." )
                break


            result.append(formatted_article)
            count +=1 

            
            if count > len(articles):
                try:
                    logger.info("Clicking 'Show More'")
                    show_more_xpath:str = 'xpath:/html/body/div[1]/div/div[3]/div/div/div/div/main/div[2]/div[2]/button'
                    self.click_xpath(show_more_xpath)

                    self.driver.wait_until_element_is_visible(show_more_xpath,30) #wait for update
                except Exception as e:
                    logger.info(f"Exhausted results - {e} ")
                    stop_parsing = True 
                    break


        return result 
             

    # add retry
    def format_article(self, article_number:int, search_phrase:str)->dict:
        """
        extracts values from news article and returns dictionary format

        Args:
            article_number (int): index of the article to be formatted
            search_phrase (str): search phrase input

        Returns:
            _type_ (dict): formatted dictionary containing expected response values
        """
        formatted_article:dict = {}
        try:
            article_xpath:str = f'xpath://*[@id="main-content-area"]/div[2]/div[2]/article[{article_number}]'
            article = self.driver.find_element(article_xpath)
            inner_html:str = article.get_attribute('innerHTML')
            formatted_article = extract_values_from_article_html(inner_html, search_phrase=search_phrase)
        except Exception as e:
            logger.error(f"Exception occurred while formating article {article_number} -- {e}")
        finally:
            return formatted_article

