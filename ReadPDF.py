import pdfplumber
import re
from FindAllPDF import find_ext
from datetime import datetime
from AddToSheets import MainAddToSheets 
import sys

Discover={}
Amex={}


def readfile(listAllPDF):
    for path in listAllPDF:
        with pdfplumber.open(path) as pdf:

            firstPage=pdf.pages[0]
            bbox = (25, 20, 400, 300)

            cropped_page = firstPage.within_bbox(bbox)
            extracted_text=cropped_page.extract_text()

            pattern = r"(New\s?Balance|NewBalance)\s*[:]?\s*\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"
            matchBalance=re.search(pattern,extracted_text)
            # if(matchBalance):
            #     print(f"Matched text: {matchBalance.group(1)}, Dollar value: {matchBalance.group(2)}")
            
            matchDiscover=re.search(r"DISCOVER",extracted_text)
            if(matchDiscover):
                #print("This is Discover")
                pattern = r"AccountSummary \d{2}/\d{2}/\d{4} -(\d{2}/\d{2}/\d{4}) PaymentInfor"
                matchDate = re.search(pattern, extracted_text)
                if matchDate:
                    second_date = matchDate.group(1)
                    #print(f"End date: {second_date}")
                    Discover[second_date]=matchBalance.group(2)
            
            matchAMEX=re.search(r"American Express",extracted_text)
            
            if(matchAMEX):
                #print("This is AMEX")
                pattern = r"Closing Date\s*(\d{2}/\d{2}/\d{2})"
                matchDate = re.search(pattern, extracted_text)
                if matchDate:
                    second_date = matchDate.group(1)
                    #print(f"End date: {second_date}")
                    Amex[second_date]=matchBalance.group(2)
            
            


            

if __name__ == '__main__':
    listAllPDF=find_ext("./documents","pdf")
    readfile(listAllPDF)
    command=sys.argv[1]
    SpreadSheetName=""
    if(command=='-n'):
        SpreadSheetName=sys.argv[2]

    SpreadSheetID=""
    if(command == '-c'):
        SpreadSheetID=sys.argv[2]
    #print(Discover)
    Discover = sorted(Discover.items(), key = lambda x:datetime.strptime(x[0], '%d/%m/%Y'), reverse=False)
    #print(Discover)
    MainAddToSheets(Discover, command, "Discover",SpreadSheetName, SpreadSheetID)
    # print(Amex)
    Amex = sorted(Amex.items(), key = lambda x:datetime.strptime(x[0], '%d/%m/%y'), reverse=False)
    #print(Amex)
    MainAddToSheets(Amex, "-p", "Amex",SpreadSheetName, SpreadSheetID)