import os, pickle 

from googleapiclient.discovery      import build 
from google_auth_oauthlib.flow      import InstalledAppFlow 
from google.auth.transport.requests import Request 

def create_api_auth(pickle_file_name: str, secret_file_path: str):
    def check_if_token_exists():
        credit = None 
        
        if (os.path.exists(pickle_file_name)):
            with open(pickle_file_name, "rb") as token:
                credit = pickle.load(token)

        return credit 
    
    def check_token_validity():
        credit_token = check_if_token_exists()
        boolean_flag = True if (not credit_token or not credit_token.valid) else False

        if (boolean_flag):
            if ((credit_token) and (credit_token.expired) and (credit_token.refresh_token)):
                credit_token.refresh(Request())
            else:
                flow_object  = InstalledAppFlow.from_client_secrets_file(secret_file_path)
                credit_token = flow_object.run_local_server(port = 0)

            with open(pickle_file_name, "wb") as token:
                pickle.dump(credit_token, token)

        return credit_token
        
    return build("gmail", "v1", credentials = check_token_validity())
