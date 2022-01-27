from bs4 import BeautifulSoup
import requests
import json
import xlsxwriter
row=0
workbook = xlsxwriter.Workbook('Stigs.xlsx')
worksheet = workbook.add_worksheet()
def get_stigs():
    url = "https://www.stigviewer.com/stigs"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    for link in soup.find_all("a"):
        stig = str(link.get("href")).split("/")
        if "stig" in stig:
            stig_title=link.text
            stig_url="https://www.stigviewer.com/{}".format(link.get("href"))
            get_json_file(stig_url,stig_title)
def get_json_file(stig_url,stig_title):
    html_content = requests.get(stig_url).text
    soup = BeautifulSoup(html_content, "lxml")
    for link in soup.find_all("a"):
        stig = str(link.get("href")).split("/")
        if "json" in stig:
            json_url = "https://www.stigviewer.com/{}".format(link.get("href"))
            data = requests.get(json_url).text
            stigobj = json.loads(data)
            findings = stigobj['stig']['findings']
            create_xls(findings,stig_title,stig_url)
def create_xls(findings,stig_title,stig_url):
    listOfGlobals = globals()
    col=0
    for item in findings:
        row_func = listOfGlobals['row']
        listOfGlobals['row']+= 1
        worksheet.write(row_func, col, stig_title)
        worksheet.write(row_func, col + 1, findings[item]['id'])
        worksheet.write(row_func, col + 2, findings[item]['severity'])
        worksheet.write(row_func, col + 3, findings[item]['title'])
        worksheet.write(row_func, col + 4, findings[item]['description'])
        worksheet.write(row_func, col + 5, stig_url)
get_stigs()
workbook.close()