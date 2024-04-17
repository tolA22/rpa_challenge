

from typing import Optional
from RPA.Browser.Selenium import Selenium 



class BaseDriver(object):

    def __init__(self,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
        disable_images: Optional[bool] = False,
        ) -> None:
        self.driver:Selenium =  Selenium() 



    def click_xpath(self, xpath:str, wait_time:Optional[int] = 10, wait_till_element_is_visible:Optional[bool] = True):
        # raise exception
        if wait_till_element_is_visible:
            self.driver.wait_until_element_is_visible(xpath, wait_time)
        web_element = self.driver.find_element(xpath)
        self.driver.click_element_when_clickable(web_element)

    def input_xpath(self,xpath:str, value:any):
        self.driver.wait_until_element_is_visible(xpath, 10)
        web_element = self.driver.find_element(xpath)
        self.driver.input_text_when_element_is_visible(web_element, value)