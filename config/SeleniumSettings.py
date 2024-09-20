from selenium import webdriver

from selenium.webdriver                import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by      import By 
from selenium.webdriver.common.keys    import Keys
from selenium.webdriver.support        import expected_conditions as ec
from selenium.webdriver.support.ui     import WebDriverWait       as wb

class SeleniumSettings:
    def __init__(self, driver_path: str, max_wait_time: int) -> None:
        self.__driver_path   = driver_path
        self.__max_wait_time = max_wait_time

        self.key_options = {
            "end"   : Keys.END, 
            "enter" : Keys.ENTER,
            "home"  : Keys.HOME
        }

    def driver_settings(self, added_options: list[str] = None):
        self.options = webdriver.ChromeOptions()
        self.service = Service(self.__driver_path)

        options_list = [
            "window-size=1920x1080",        
            "disable-gpu", 
            "start-maximized",
            "ignore-certificate-errors",
            "lang=en",
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36"
        ]

        options_list = options_list + added_options if type(added_options) == list else options_list

        for i in options_list:
            self.options.add_argument(i)

        self.driver   = webdriver.Chrome(options = self.options, service = self.service)        
        self.__wait   = wb(self.driver, self.__max_wait_time)
        self.__action = ActionChains(self.driver)
    
    def wait_for_element(self, element_str: str, element_type: str = "class"):
        match element_type.lower():
            case "xpath" : self.__wait.until(ec.presence_of_all_elements_located((By.XPATH, element_str)))
            case "id"    : self.__wait.until(ec.presence_of_all_elements_located((By.ID, element_str)))
            case "class" : self.__wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, element_str)))
            case _       : raise RuntimeError("Unsupported element type")
        
    def wait_for_element_to_be_visible(self, element_str: str, element_type: str = "class"):
        match element_type.lower():
            case "xpath" : self.__wait.until(ec.visibility_of_all_elements_located((By.XPATH, element_str)))
            case "id"    : self.__wait.until(ec.visibility_of_all_elements_located((By.ID, element_str)))
            case "class" : self.__wait.until(ec.visibility_of_all_elements_located((By.CLASS_NAME, element_str)))
            case _       : raise RuntimeError("Unsupported element type")

    def wait_for_element_and_return_element(self, element_str: str, element_type: str = "class"):
        return_value = ""

        match element_type.lower():
            case "xpath": 
                self.__wait.until(ec.presence_of_all_elements_located((By.XPATH, element_str)))
                return_value = self.driver.find_element(By.XPATH, element_str)
            case "id": 
                self.__wait.until(ec.presence_of_all_elements_located((By.ID, element_str)))
                return_value = self.driver.find_element(By.ID, element_str)
            case "class": 
                self.__wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, element_str)))
                return_value = self.driver.find_element(By.CLASS_NAME, element_str)
            case _: 
                raise RuntimeError("Unsupported element type")
            
        return return_value
    
    def wait_for_elements_and_return_elements(self, element_str: str, element_type: str = "class"):
        return_value = ""

        match element_type.lower():
            case "xpath": 
                self.__wait.until(ec.presence_of_all_elements_located((By.XPATH, element_str)))
                return_value = self.driver.find_elements(By.XPATH, element_str)
            case "id": 
                self.__wait.until(ec.presence_of_all_elements_located((By.ID, element_str)))
                return_value = self.driver.find_elements(By.ID, element_str)
            case "class": 
                self.__wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, element_str)))
                return_value = self.driver.find_elements(By.CLASS_NAME, element_str)
            case _: 
                raise RuntimeError("Unsupported element type")
            
        return return_value
    
    def wait_for_element_to_be_visible_and_return_element(self, element_str: str, element_type: str = "class"):
        return_value = ""

        match element_type.lower():
            case "xpath": 
                self.__wait.until(ec.visibility_of_element_located((By.XPATH, element_str)))
                return_value = self.driver.find_element(By.XPATH, element_str)
            case "id": 
                self.__wait.until(ec.visibility_of_element_located((By.ID, element_str)))
                return_value = self.driver.find_element(By.ID, element_str)
            case "class": 
                self.__wait.until(ec.visibility_of_element_located((By.CLASS_NAME, element_str)))
                return_value = self.driver.find_element(By.CLASS_NAME, element_str)
            case _: 
                raise RuntimeError("Unsupported element type")
            
        return return_value
    
    def wait_for_elements_to_be_visible_and_return_elements(self, element_str: str, element_type: str = "class"):
        return_value = ""

        match element_type.lower():
            case "xpath": 
                self.__wait.until(ec.visibility_of_element_located((By.XPATH, element_str)))
                return_value = self.driver.find_elements(By.XPATH, element_str)
            case "id": 
                self.__wait.until(ec.visibility_of_element_located((By.ID, element_str)))
                return_value = self.driver.find_elements(By.ID, element_str)
            case "class": 
                self.__wait.until(ec.visibility_of_element_located((By.CLASS_NAME, element_str)))
                return_value = self.driver.find_elements(By.CLASS_NAME, element_str)
            case _: 
                raise RuntimeError("Unsupported element type")
            
        return return_value
    
    def wait_for_element_to_be_clickable(self, element_str: str, element_type: str = "class"):
        match element_type.lower():
            case "xpath" : self.__wait.until(ec.element_to_be_clickable((By.XPATH, element_str)))
            case "id"    : self.__wait.until(ec.element_to_be_clickable((By.ID, element_str)))
            case "class" : self.__wait.until(ec.element_to_be_clickable((By.CLASS_NAME, element_str)))

    def check_for_element(self, element_str: str, element_type: str = "class"):
        return_value = False

        match element_type.lower():
            case "xpath" : return_value = len(self.driver.find_elements(By.XPATH, element_str)) > 0
            case "id"    : return_value = len(self.driver.find_elements(By.ID, element_str)) > 0
            case "class" : return_value = len(self.driver.find_elements(By.CLASS_NAME, element_str)) > 0
            case _       : raise RuntimeError("Unsupported element type")

        return return_value
    
    def search_for_element(self, element_str: str, element_type: str = "class"):
        match element_type.lower():
            case "xpath" : return_value = self.driver.find_element(By.XPATH, element_str)
            case "id"    : return_value = self.driver.find_element(By.ID, element_str)
            case "class" : return_value = self.driver.find_element(By.CLASS_NAME, element_str)
            case _       : raise RuntimeError("Unsupported element type")
        
        return return_value 
    
    def search_for_elements(self, element_str: str, element_type: str = "class"):
        match element_type.lower():
            case "xpath" : return_value = self.driver.find_elements(By.XPATH, element_str)
            case "id"    : return_value = self.driver.find_elements(By.ID, element_str)
            case "class" : return_value = self.driver.find_elements(By.CLASS_NAME, element_str)
            case _       : raise RuntimeError("Unsupported element type")

        return return_value
    
    def click_on_element(self, element_str: str, element_type: str = "class"):
        match element_type.lower():
            case "xpath" : self.driver.find_element(By.XPATH, element_str).click()
            case "id"    : self.driver.find_element(By.ID, element_str).click()
            case "class" : self.driver.find_element(By.CLASS_NAME, element_str).click()
            case _       : raise RuntimeError("Unsupported element type")

    def wait_and_send_string_to_element(self, keyword: str, element_str: str, element_type: str = "class"):
        match element_type.lower():
            case "xpath":
                self.__wait.until(ec.presence_of_all_elements_located((By.XPATH, element_str)))
                self.driver.find_element(By.XPATH, element_str).send_keys(keyword)
            case "id":
                self.__wait.until(ec.presence_of_all_elements_located((By.ID, element_str)))
                self.driver.find_element(By.ID, element_str).send_keys(keyword)
            case "class":
                self.__wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, element_str)))
                self.driver.find_element(By.CLASS_NAME, element_str).send_keys(keyword)
            case _:
                raise RuntimeError("Unsupported element type")
    
    def send_keys_to_element(self, key_strings: str, element_str: str, element_type: str = "class"):
        match element_type.lower():
            case "xpath" : self.driver.find_element(By.XPATH, element_str).send_keys(self.key_options[key_strings.lower()])
            case "id"    : self.driver.find_element(By.ID, element_str).send_keys(self.key_options[key_strings.lower()])
            case "class" : self.driver.find_element(By.CLASS_NAME, element_str).send_keys(self.key_options[key_strings.lower()])
            case _       : raise RuntimeError("Unsupported element type")

    def check_if_element_is_clickable(self, element_str: str, element_type: str = "class"):
        def try_clicking(element_method: By, element_str: str):
            try:
                self.driver.find_element(element_method, element_str).click()
                clickable_yn = True 
            except:
                pass

            return clickable_yn

        clickable_yn = False

        match element_type.lower():
            case "xpath" : clickable_yn = try_clicking(By.XPATH, element_str)
            case "id"    : clickable_yn = try_clicking(By.ID, element_str)
            case "class" : clickable_yn = try_clicking(By.CLASS_NAME, element_str)
            case _       : raise RuntimeError("Unsupported element type")

        return clickable_yn
    
    def click_on_element(self, element_str: str, element_type: str = "class"):
        match element_type.lower():
            case "xpath" : self.__action.click(self.driver.find_element(By.XPATH, element_str)).perform()
            case "id"    : self.__action.click(self.driver.find_element(By.ID, element_str)).perform()
            case "class" : self.__action.click(self.driver.find_element(By.CLASS_NAME, element_str)).perform()
            case _       : raise RuntimeError("Unsupported element type")
