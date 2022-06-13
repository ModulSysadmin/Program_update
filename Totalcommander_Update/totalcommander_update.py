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
URL = 'https://www.ghisler.com/download.htm'

def check_old_version_32bit_1():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\totalcmd\\TOTALCMD.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version
def check_old_version_64bit_1():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\totalcmd\\TOTALCMD64.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version
def check_old_version_32bit_2():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files (x86)\\totalcmd\\TOTALCMD.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version
def check_old_version_64bit_2():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files (x86)\\totalcmd\\TOTALCMD64.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version

def get_html(url):
    r = requests.get(url)
    return r

def get_html_text(url):
    r = requests.get(url)
    return r.text

def check_new_version(html):
    soup = BeautifulSoup(html, 'html.parser')
    txt = soup.find("h3")
    txt1 = txt.text
    full_version = txt1.split(' ')
    version = full_version[9]
    new_version = version[:-1]
    if(os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD.EXE")):
        old_version_1 = check_old_version_32bit_1()
    elif(os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD64.EXE")):
        old_version_1 = check_old_version_64bit_1()
    elif(os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD.EXE")):
        old_version_1 = check_old_version_32bit_2()
    elif(os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD64.EXE")):
        old_version_1 =check_old_version_64bit_2()

    if old_version_1[3] == ".":
        old_version = old_version_1[0] + old_version_1[1] + old_version_1[2]
    else:
        old_version = old_version_1[0] + old_version_1[1] + old_version_1[2] + old_version_1[3]
    print(f"Old version - {old_version}")
    print(f"New version - {new_version}")
    file1 = open("old_version.txt","w+")
    file2 = open("new_version.txt","w+")
    file1.write(old_version)
    file2.write(new_version)
    file1.close()
    file2.close()
    time.sleep(1)

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

def get_download_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a'): 
        urls.append(link.get('href'))
    return urls[16]


if __name__ == "__main__":
    if(os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD.EXE")) or (os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD64.EXE")):
        html = get_html(URL)
        if html.status_code == 200:
            check_new_version(get_html_text(URL))
            check = read_file()
            if (check):
                print("New version TotalCommander installed")
                os.remove("old_version.txt")
                os.remove("new_version.txt")
            else:
                os.mkdir("downloads")
                result_url = get_download_link(get_html_text(URL))
                Program_Name = f"{PATH}\\downloads\\TotalCommander.exe"
                print("Downloading...")
                with urllib.request.urlopen(result_url) as response, open(Program_Name, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                print("Success")
                print('Installing...')
                process = subprocess.Popen([f'{PATH}\\downloads\\TotalCommander.exe', '/AHMGDU'])
                process.wait()
                print("Success")
                os.remove(f"{PATH}\\downloads\\TotalCommander.exe")
                os.rmdir("downloads")
                os.remove("old_version.txt")
                os.remove("new_version.txt")
                print("TotalCommander update\nEnd...")
        else:
            print("Eror page")


    elif (os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD64.EXE")) or (os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD.EXE")):
        html = get_html(URL)
        if html.status_code == 200:
            check_new_version(get_html_text(URL))
            check = read_file()
            if (check):
                print("New version TotalCommander installed")
                os.remove("old_version.txt")
                os.remove("new_version.txt")
            else:
                os.mkdir("downloads")
                result_url = get_download_link(get_html_text(URL))
                Program_Name = f"{PATH}\\downloads\\TotalCommander.exe"
                print("Downloading...")
                with urllib.request.urlopen(result_url) as response, open(Program_Name, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                print("Success")
                print('Installing...')
                process = subprocess.Popen([f'{PATH}\\downloads\\TotalCommander.exe', '/AHMGDU'])
                process.wait()
                print("Success")
                os.remove(f"{PATH}\\downloads\\TotalCommander.exe")
                os.rmdir("downloads")
                os.remove("old_version.txt")
                os.remove("new_version.txt")
                print("TotalCommander update\nEnd...")
        else:
            print("Eror page")

    else:
        html = get_html(URL)
        if html.status_code == 200:
            os.mkdir("downloads")
            result_url = get_download_link(get_html_text(URL))
            Program_Name = f"{PATH}\\downloads\\TotalCommander.exe"
            print("Downloading...")
            with urllib.request.urlopen(result_url) as response, open(Program_Name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            print("Success")
            print('Installing...')
            process = subprocess.Popen([f'{PATH}\\downloads\\TotalCommander.exe', '/AHMGDU'])
            process.wait()
            print("Success")
            os.remove(f"{PATH}\\downloads\\TotalCommander.exe")
            os.rmdir("downloads")
            print("TotalCommander install\nEnd...")
        else:
            print("Eror page")

    print("Program ended....")
    exit = input()

