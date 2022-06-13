import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import platform
import shutil
import subprocess
import time
import ssl
###########################

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

###########################
PATH = os.getcwd()
url_text = 'https://notepad-plus-plus.org/'

#Function of getting html text
def get_html(url, params=None):
    r = requests.get(url,params=params)
    return r
#Function of checking old version notepad++
def check_old_version():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\Notepad++\\notepad++.exe\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version

#Function of checking new version notepad++ and write to file
def check_new_version(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('p', class_='library-desc')
    txt = items.text
    new_version = txt[17:]
    old_version = check_old_version()
    file1 = open("old_version.txt","w+")
    file2 = open("new_version.txt","w+")
    file1.write(old_version)
    file2.write(new_version)
    file1.close()
    file2.close()
    time.sleep(1)
#Function of reading file
def read_file():
    read_version_1 = open('old_version.txt')
    read_version_2 = open('new_version.txt')
    txt1 = read_version_1.read()
    txt2 = read_version_2.read()
    number_1 = float(txt1)
    number_2 = float(txt2)
    if(number_2 - number_1) == 0:
        return True
    else:
        return False
#Function of getting url page
def get_download_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a'): 
        urls.append(link.get('href'))
    url_download = urls[2]
    download_page = url_text + url_download
    return download_page

#Function of getting url download
def get_url_download(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href')) 
    url_download = urls[12]
    return url_download


if __name__ == "__main__":
    #Check of exist notepad++
    if(os.path.exists("C:\\Program Files\\Notepad++\\notepad++.exe")):
        html_1 = get_html(url_text)   
        if(html_1.status_code) == 200:
            check_new_version(html_1.text)
            check = read_file()
            if(check):
                print("New version notepad++ installed")
                os.remove("old_version.txt")
                os.remove("new_version.txt")
            else:
                os.mkdir("downloads")
                url_page = get_download_page(html_1.text)
                html_2 = get_html(url_page)
                if(html_2.status_code) == 200:
                    result_url = get_url_download(html_2.text)
                    Program_Name = f"{PATH}\\downloads\\Notepad++.exe"
                    print("Downloading...")
                    with urllib.request.urlopen(result_url) as response, open(Program_Name, 'wb') as out_file:
                        shutil.copyfileobj(response, out_file)
                    print("Installing...")
                    process = subprocess.Popen([f'{PATH}\\downloads\\Notepad++.exe', '/S'])
                    process.wait()
                    os.remove(f"{PATH}\\downloads\\Notepad++.exe")
                    os.rmdir("downloads")
                    os.remove("old_version.txt")
                    os.remove("new_version.txt")
                    print("Notepad update\nEnd...")
                else:
                    print("Eror second page")
        else:
            print('Eror first page')
    else:
        html_3 = get_html(url_text)  
        if(html_3.status_code) == 200:
            os.mkdir("downloads")
            url_page = get_download_page(html_3.text)
            html_4 = get_html(url_page)
            if(html_4.status_code) == 200:
                result_url = get_url_download(html_4.text)
                Program_Name = f"{PATH}\\downloads\\Notepad++.exe"
                print("Downloading...")
                with urllib.request.urlopen(result_url) as response, open(Program_Name, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                print("Installing...")
                process = subprocess.Popen([f'{PATH}\\downloads\\Notepad++.exe', '/S'])
                process.wait()
                os.remove(f"{PATH}\\downloads\\Notepad++.exe")
                os.rmdir("downloads")
                print("Notepad install\nEnd...")
            else:
                print("Eror second page")
        else:
            print('Eror first page') 


    exit()

