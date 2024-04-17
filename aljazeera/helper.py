


from datetime import date, datetime
import re
from typing import Optional
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import pandas as pd 
import os 
import pathlib

from aljazeera.constant import  DATE_FORMAT, FIXTURES_PATH
from aljazeera.logger import logger


def get_start_and_end_date_from_current_month(number_of_months:int)->tuple:
    """
    
    returns start_date_time and end_date_time from current date using number_of_months 

    Args:
        number_of_months (int): number of months ; 0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months

    Returns:
        tuple: start_date_time,end_date_time
    """
    current_date_time:date = date.today()
    lag_months:int = 0 if number_of_months < 2 else number_of_months - 1

    start_date_time:date = current_date_time - relativedelta(months=lag_months)

    return start_date_time.replace(day=1) , current_date_time
 

def validate_news_category(input_news_category_list:set, valid_news_category_list:set):
    """
    checks for invalid category from input list

    Args:
        input_news_category_list (list): _description_
    """
    

    #subtract the two sets
    difference:set =  input_news_category_list - valid_news_category_list
    
    if len(difference) > 0:
        raise Exception(f"Invalid category found {difference}; Valid category list are {valid_news_category_list}")
    
    return 

def clean_up_string(value:str):
    """
    
    cleans up str gotten from html tags

    Args:
        value (str): text from html tags

    Returns:
        _type_: cleaned up strings
    """
    value = value.replace("Last update","")
    return value.strip()

def extract_values_from_article_html(html_content, search_phrase:str):
    title:str = ""
    date_:str = "" 
    description:str = ""
    picture_filename:str = "" 
    count_of_search_phrases:int = 0 
    contains_money:bool = False 
    
    soup = BeautifulSoup(html_content) 

    try:
        """ 
        <h3 class="gc__title"><a href="https://www.aljazeera.com/news/2024/4/16/russia-ukraine-war-list-of-key-events-day-782" class="u-clickable-card__link"><span>Rus­sia-Ukraine war: List of key events, day 782 | Rus­sia-Ukraine ...</span></a></h3>
        """
        logger.info("Extracting title")
        #extracting title
        gc_title = soup.find_all('h3',{"class":"gc__title"})[0]
        title_span  = gc_title.find_all('span')[0]
        title:str = clean_up_string(title_span.text)
    except Exception as e:
        logger.error(f"Error extracting title -- {e}") 

    try:    
        """ 
        <div class="gc__body-wrap"><div class="gc__excerpt"><p>1 day ago ... Here is the sit­u­a­tion on Tues­day, April 16, 2024. Fight­ing. At least two peo­ple were killed af­ter a Russ­ian guid­ed aer­i­al bomb hit an ed­u­ca­tion&nbsp;...</p></div></div>
        """

        logger.info("Extracting description")
        #extracting description
        gc__body_wrap = soup.find_all('div',{"class":"gc__body-wrap"})[0]
        gc__excerpt  = gc__body_wrap.find_all('div',{"class":"gc__excerpt"})[0]
        description_p = gc__excerpt.find_all('p')[0]
        description:str = clean_up_string(description_p.text)
    except Exception as e:
        logger.error(f"Error extracting description -- {e}") 

    try:
        """ 
        <footer class="gc__footer"><div class="gc__meta"><div class="gc__date gc__date--published"><div class="gc__date__date"><div class="date-simple css-1yjq2zp"><span class="screen-reader-text">Published On 16 Apr 2024</span><span aria-hidden="true">16 Apr 2024</span></div></div></div></div></footer>
        17 April 2024
        """

        logger.info("Extracting date")
        #extracting date
        gc__footer = soup.find_all('footer',{"class":"gc__footer"})[0]
        gc__date__date  = gc__footer.find_all('div',{"class":"gc__date__date"})[0]
        date_simple = gc__date__date.find_all('div',{'class':'date-simple'})[0]
        date_span = date_simple.find_all('span')[1]
        date_:str = clean_up_string(date_span.text)
    except Exception as e:
        logger.error(f"Error extracting date -- {e}") 
        date_ = date.today().strftime(DATE_FORMAT)

    try:
        """ 
        <div class="gc__image-wrap"><div class="article-card__image-wrap article-card__featured-image" tabindex="-1" aria-hidden="false"><div class="responsive-image"><img class="article-card__image gc__image" loading="lazy" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQELw_na0ZMrTXoCmLuhfl1h1Iq27va2T1lnsLOvhgo71vCVwc_VRA-aTvf&amp;s&amp;resize=770%2C513&amp;quality=80" srcset="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQELw_na0ZMrTXoCmLuhfl1h1Iq27va2T1lnsLOvhgo71vCVwc_VRA-aTvf&amp;s&amp;quality=80 270w, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQELw_na0ZMrTXoCmLuhfl1h1Iq27va2T1lnsLOvhgo71vCVwc_VRA-aTvf&amp;s&amp;resize=140%2C93&amp;quality=80 140w, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQELw_na0ZMrTXoCmLuhfl1h1Iq27va2T1lnsLOvhgo71vCVwc_VRA-aTvf&amp;s&amp;resize=170%2C113&amp;quality=80 170w, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQELw_na0ZMrTXoCmLuhfl1h1Iq27va2T1lnsLOvhgo71vCVwc_VRA-aTvf&amp;s&amp;resize=375%2C250&amp;quality=80 375w, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQELw_na0ZMrTXoCmLuhfl1h1Iq27va2T1lnsLOvhgo71vCVwc_VRA-aTvf&amp;s&amp;resize=570%2C380&amp;quality=80 570w, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQELw_na0ZMrTXoCmLuhfl1h1Iq27va2T1lnsLOvhgo71vCVwc_VRA-aTvf&amp;s&amp;resize=770%2C513&amp;quality=80 770w" sizes="(max-width: 270px) 270px, (max-width: 140px) 140px, (max-width: 170px) 170px, (max-width: 375px) 375px, (max-width: 570px) 570px, (max-width: 770px) 770px, 770px" alt="A Ukrainian soldier smoking a cigarette on the frontline" pinger-seen="true"></div></div></div>
        """

        logger.info("Extracting picture src")
        #extracting date
        gc__image_wrap = soup.find_all('div',{"class":"gc__image-wrap"})[0]
        gc__image  = gc__image_wrap.find_all('img',{"class":"gc__image"})[0]
        picture_filename:str = gc__image["src"]
    except Exception as e:
        logger.error(f"Error extracting date -- {e}") 


    match_str = f"{title}\n{description}"
    try:
        matches:list = re.findall(r"\$[\d,.]+", match_str)  #checking for $11 cases
        matches_dollar:list = re.findall(r"\s*[\d,.]+\s*(?:dollar|usd)", match_str, re.IGNORECASE)
        if matches or matches_dollar:
            contains_money = True 
        
    except Exception as e:
        logger.error(f"Error checking  contains_money -- {e}") 


    try:
        matches:list = re.findall(rf"{search_phrase}", match_str, re.IGNORECASE)
        if matches:
            count_of_search_phrases = len(matches)  
    except Exception as e:
        logger.error(f"Error extracting count_of_search_phrases -- {e}") 

    return {
        "title":title,
        "date":date_,
        "description":description,
        "picture_filename":picture_filename,
        "count_of_search_phrases":count_of_search_phrases,
        "contains_money":contains_money
    }



def save_dataframe(dataframe:pd.DataFrame):
    """
    
    saves dataframe as csv and excel

    Args:
        dataframe (pd.DataFrame): _description_
    """
    os.makedirs(FIXTURES_PATH, exist_ok=True) 
    dataframe.to_csv(f'{FIXTURES_PATH}/news_report.csv', index=False)
    dataframe.to_excel(f'{FIXTURES_PATH}/news_report.xlsx', index=False)