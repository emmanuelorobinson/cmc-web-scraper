import requests
import pandas as pd
from bs4 import BeautifulSoup

def main():
    # open the excel file
    excel = pd.ExcelFile('coinmarketcap.xlsx')

    # get the first sheet
    df = excel.parse(0)

    # write to rows beneth the first column
    
    list = initalPageRequest('1')
    pageList=[]

    for i in list:
        # append to subsequent rows under the first column
        # ensure no duplicate entries
        pageList.append(getCoinURL(i))

        if i not in df['Link']:
            df.loc[len(df)] = [i]

    for i in pageList:
        for j in i:
            getCoinEmail(j)
        
    # save the file
    df.to_excel('coinmarketcap.xlsx', sheet_name='Sheet1', index=False)

def initalPageRequest(page):
    url = 'https://coinmarketcap.com/coins/?page='+page
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    webLink=[]


    # find all href links with class cmc-link under class sc-16r8icm-0
    for link in soup.find_all('a', class_='cmc-link'):
        # if the href link starts with /currencies/
        if link.get('href').startswith('/currencies/'):
            # add the href link to the list
            webLink.append(link.get('href'))

    return webLink

def getCoinURL(url):
    url = 'https://coinmarketcap.com'+url
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    pageLink=[]
    # find all href links with class cmc-link under class sc-16r8icm-0
    for link in soup.find_all('a', class_='link-button'):
        # get the href link
        pageLink.append(link.get('href'))

    return pageLink

def getCoinEmail(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    email=[]

    # find all mailto links
    for link in soup.find_all('a'):
        # get the href link
        # check if mailto
        try:
            if link.get('href').startswith('mailto:'):
                print(link.get('href'))
        except:
            pass



if __name__ == '__main__':
    main()


