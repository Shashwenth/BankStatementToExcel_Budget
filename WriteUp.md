Documentation :

>Attempts:

1. Tried to use package pdf-statement-reader. Failed to read the documents and the offical documentions mentions that it is a CLI tool.
Unable to find proper documentions.

2. PyPDF2. Improper scan. Did not have proper results. 

3. PDfplumber. Highly rated. Scanned the documents well, atleast in the specified box. Did not try box for previous versions but since this worked
did not bother to try the box in the other two libraries.


>Regex:

Regex for hard coded mapping. THis is because the Discover and AMEX scans produced unique styles of data.

> Excel:
Used the Same Spreadsheet API that I used for satish mama's project.

P.S: If we need to add new bank data, then we need to hard code even more unique regex.



HOW TO RUN:

1. Activate the venv 
2. Create a Google service account and give access to spreadsheet API, Drive API acess.
3. Download the google-json-cred from the google 
4. Add them to the root folder
5. Add the statements into the ./documents
6. pip install the following:
    >pdfplumber
    >google-auth
    >google-api-python-client
6. For a new SpreadSheet
>python ReadPDF.py -n SpreadSheetName
For the previous SpreadSheet
>python ReadPDF.py -p
For a custom spreadSheet ID
>python ReadPDF.py -c SpreadSheetID


