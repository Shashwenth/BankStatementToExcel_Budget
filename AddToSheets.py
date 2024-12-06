import sys
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import json
import os
from dotenv import load_dotenv

load_dotenv()
Details=[]
email=os.getenv("email")

'''
Function to create a spreadsheet of the mentioned Title.
And share it with personal ID
'''

def create_spreadsheet(title):
    key_path = "google-json-cred.json" 

    creds = service_account.Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])

    try:
        sheets_service = build("sheets", "v4", credentials=creds)

        spreadsheet = {"properties": {"title": title}}

        response = sheets_service.spreadsheets().create(body=spreadsheet, fields="spreadsheetId").execute()
        
        spreadsheet_id = response.get("spreadsheetId")
        #print(f"Spreadsheet created with ID: {spreadsheet_id}")

        drive_service = build("drive", "v3", credentials=creds)
        permission = {
            "type": "user",
            "role": "writer",  
            "emailAddress": email  # Share with your email
        }

        drive_service.permissions().create(fileId=spreadsheet_id, body=permission, fields="id").execute()
        

        return spreadsheet_id

    except HttpError as error:
        #print(f"An error occurred: {error}")
        return None


'''
Funtion to create a new Sheet with the fileName 
'''
def AddNewSheet(spreadsheetId, worksheetName):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'google-json-cred.json'
    SPREADSHEET_ID = spreadsheetId

    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build("sheets", "v4", credentials=creds)

    batch_update_values_request_body = {
            'requests': [
                {
                    'addSheet': {
                        'properties': {
                            'title': worksheetName
                        }
                    }
                }
            ]
        }
    request = service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=batch_update_values_request_body)
    response = request.execute()



'''
TO check is the spreadsheet ID is valid 
'''
def CheckIfSpreadsheetExists(spreadSheet_ID):
    key_path = "google-json-cred.json" 
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    try:
        sheets_service = build("sheets", "v4", credentials=creds)
        response= sheets_service.spreadsheets().get(
            spreadsheetId=spreadSheet_ID
        ).execute()

        if(response):
            #print(response)
            #print("SpreadSheet Already Exist")
            return True
        else:
            #print("Need to create a new spreadsheet")
            return False

    except HttpError as error:
        print(f"An error occurred: {error}")



'''
Check if the particular sheet name is valid 
'''
def checkIfSheetExist(spreadSheet_ID, sheetName):
    key_path = "google-json-cred.json" 
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    try:
        sheets_service = build("sheets", "v4", credentials=creds)
        response= sheets_service.spreadsheets().get(
            spreadsheetId=spreadSheet_ID
        ).execute()
        #print(response.get('sheets'))
        #print([i.get('properties').get('title') for i in response.get('sheets')])
        if(sheetName in [i.get('properties').get('title') for i in response.get('sheets')]):
            #print(response)
            #print("Sheet Already Exist")
            return True
        else:
            #print("Need to create a new spreadsheet")
            return False

    except HttpError as error:
        print(f"An error occurred: {error}")



'''
Append the data to a specific spreadsheet 
'''
def append_data_to_specific_sheet(spreadsheet_id, sheet_name, Details):
    key_path = "google-json-cred.json" 
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    
    try:
        sheets_service = build("sheets", "v4", credentials=creds)

        range_ = f"{sheet_name}"
        body = {
            "values": [[item[0], item[1]] for item in Details] 
        }

        result = sheets_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_,
            valueInputOption="RAW", 
            body=body,
            insertDataOption="INSERT_ROWS" 
        ).execute()


    except HttpError as error:
        print(f"An error occurred: {error}")


def GetspreadSheetId():
    file = open('RobinhoodSpreadSheetIDStore.txt','r')
    sID=file.readline().strip()
    file.close()
    return sID


def WriteSpreadSheetID(spreadSheetID):
    file = open('RobinhoodSpreadSheetIDStore.txt','w')
    file.writelines(spreadSheetID)
    file.close()
    

def MainAddToSheets(details, command, BankName, SpreadSheetName, spreadSheetID):
    Details=details
    #print(Details)
    if(command=="-n"):
        spreadSheet_ID=create_spreadsheet(SpreadSheetName)
        WriteSpreadSheetID(spreadSheet_ID)
        if(CheckIfSpreadsheetExists(spreadSheet_ID)):
            #print("SpreadSheet already exist")
            if(checkIfSheetExist(spreadSheet_ID, BankName)):
                #print("Sheet already exist")
                append_data_to_specific_sheet(spreadSheet_ID, BankName, Details)
            else:
                AddNewSheet(spreadSheet_ID,BankName)
                append_data_to_specific_sheet(spreadSheet_ID, BankName, Details=[("Date","Amount")])
                append_data_to_specific_sheet(spreadSheet_ID, BankName, Details)

    if(command=="-p"):
        spreadSheet_ID=GetspreadSheetId()
        if(CheckIfSpreadsheetExists(spreadSheet_ID)):
            #print("SpreadSheet already exist")
            if(checkIfSheetExist(spreadSheet_ID, BankName)):
                #print("Sheet already exist")
                append_data_to_specific_sheet(spreadSheet_ID, BankName, Details)
            else:
                AddNewSheet(spreadSheet_ID,BankName)
                append_data_to_specific_sheet(spreadSheet_ID, BankName, Details=[("Date","Amount")])
                append_data_to_specific_sheet(spreadSheet_ID, BankName, Details)

    if(command=="-c"):
        spreadSheet_ID=spreadSheetID
        if(CheckIfSpreadsheetExists(spreadSheet_ID)):
            #print("SpreadSheet already exist")
            if(checkIfSheetExist(spreadSheet_ID, BankName)):
                #print("Sheet already exist")
                append_data_to_specific_sheet(spreadSheet_ID, BankName, Details)
            else:
                AddNewSheet(spreadSheet_ID,BankName)
                append_data_to_specific_sheet(spreadSheet_ID, BankName, Details=[("Date","Amount")])
                append_data_to_specific_sheet(spreadSheet_ID, BankName, Details)
                

