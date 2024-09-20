import os, base64, pytz, shutil, json, html, time, logging 

import datetime as dt 

from bs4 import BeautifulSoup as bs4

from config.SeleniumSettings                 import SeleniumSettings 
from miscellaneous_functions.create_api_auth import create_api_auth

class InterceptGmail:    
    def __init__(self, pickle_file_name: str, secret_file_path: str, driver_path: str, max_wait_time: int):
        self.__pickle_file_name = pickle_file_name 
        self.__secret_file_path = secret_file_path 
        self.current_date       = dt.datetime.now().date()
        self.selenium_object    = SeleniumSettings(driver_path, max_wait_time)
        self.selenium_object.driver_settings(["--headless=new"])

    def intercept_gmail_settings_method(self, log_file_name: str, download_path: str, repository_path: str, timezone_string: str, mail_keywords: list[str]):
        self.download_path   = download_path 
        self.repository_path = repository_path
        self.mail_keywords   = mail_keywords 
        self.timezone_object = pytz.timezone(timezone_string)
        self.gmail_service   = create_api_auth(self.__pickle_file_name, self.__secret_file_path)
        os.makedirs(os.path.join(self.repository_path, str(self.current_date)), exist_ok = True)
        logging.basicConfig(
            filename = log_file_name.format(str(dt.datetime.now(self.timezone_object))[0:19].replace(":", "")),
            filemode = "a",
            format   = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            encoding = "utf-8"
        )

        self.data_log_object = logging.getLogger("Gmail Interceptor Log")
        self.data_log_object.setLevel(logging.DEBUG)
        self.data_log_object.info(f"{str(dt.datetime.now(self.timezone_object))} - Gmail Interception operations")

    def __get_email_ids(self):
        email_ids_list, page_token = [], None 
        self.data_log_object.info(f"{str(dt.datetime.now(self.timezone_object))} -----------------------------LINE BREAK-----------------------------")
        self.data_log_object.info(f"{str(dt.datetime.now(self.timezone_object))} - Extracting email ids")

        while (True):
            response   = self.gmail_service.users().messages().list(userId = "me", pageToken = page_token).execute()
            ids_list   = [inner_json["id"] for inner_json in response["messages"]]
            page_token = response.get("nextPageToken", None)
            email_ids_list.extend(ids_list)

            if (page_token is None):
                self.data_log_object.info(f"{str(dt.datetime.now(self.timezone_object))} - Email ids extracted")
                break 

        return email_ids_list
    
    def __get_email_object(self):
        ids_list, objects_list = self.__get_email_ids(), []

        for keyword in self.mail_keywords:            
            self.data_log_object.info(f"{str(dt.datetime.now(self.timezone_object))} - Searching for email containing '{keyword}'")

            for message_id in ids_list: 
                response = self.gmail_service.users().messages().get(id = message_id, userId = "me").execute()
                snippet  = html.unescape(response["snippet"])

                if (keyword.lower() in snippet.lower()):
                    objects_list.append(response)
                    self.data_log_object.info(f"{str(dt.datetime.now(self.timezone_object))} - Email containing '{keyword}' found")
                    break   

        return objects_list
    
    def __wait_until_file_is_downloaded(self, file_date_name: str):
        file_flag = False 

        while (file_flag != True):
            file_flag = os.path.exists(os.path.join(self.download_path, file_date_name))
            time.sleep(3)

            if (file_flag == True):
                shutil.unpack_archive(os.path.join(self.download_path, file_date_name), os.path.join(self.repository_path, str(dt.datetime.now(self.timezone_object).date())))
                self.data_log_object.info(f"{str(dt.datetime.now(self.timezone_object))} - Data file relocated to {self.repository_path}")
    
    def download_file(self):
        objects_list = self.__get_email_object()

        for object in objects_list:
            file_date_name = f'{str(dt.datetime.fromtimestamp(float(object["internalDate"]) / 1000, self.timezone_object).date()).replace("-", "")}.zip'
            inner_response = base64.urlsafe_b64decode(object["payload"]["parts"][0]["parts"][0]["body"]["data"]).decode("utf-8")
            download_link  = bs4(inner_response, "html.parser").find_all(href = True)[1]["href"]
            self.data_log_object.info(f"{str(dt.datetime.now(self.timezone_object))} - Downloading data file {file_date_name}")
            self.selenium_object.driver.get(download_link)
            self.__wait_until_file_is_downloaded(file_date_name)
            os.remove(os.path.join(self.download_path, file_date_name))

if (__name__ == "__main__"):
    with open("./config/InterceptGmailConfig.json", "r", encoding = "utf-8") as f:
        config_dict = json.load(f)

    intercept_gmail = InterceptGmail(**config_dict["InterceptGmail"]["constructor"])
    intercept_gmail.intercept_gmail_settings_method(**config_dict["InterceptGmail"]["intercept_gmail_settings_method"])
    intercept_gmail.download_file()
