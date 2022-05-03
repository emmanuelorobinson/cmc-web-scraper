import requests
import pandas as pd
from bs4 import BeautifulSoup

def main():

    for l in range(13,15):
    #change l to string
        page = str(l)
        list = initalPageRequest(page)
        pageList=[]

        for i in list:
            pageList.append(getCoinURL(i))

        recursionHelper(pageList)

        print('Page: ' + page)
        
    # save the file


def recursionHelper(website):
    
    try:
        for i in website:
            print('')
            if isinstance(i, list):
                # recursion
                print('List')
                recursionHelper(i)
            else:
                # get the coin email
                if i.endswith('.pdf'):
                    return None
                getCoinEmail(i)
    except:
        pass

    

def initalPageRequest(page):
    url = 'https://coinmarketcap.com/coins/?page='+page
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    webLink=[]


    # find all href links with class cmc-link under class sc-16r8icm-0
    for link in soup.find_all('a', class_='cmc-link'):
        # if the href link starts with /currencies/
        try:
            if link.get('href').startswith('/currencies/'):
                # add the href link to the list
                webLink.append(link.get('href'))
            else:
                pass

        except AttributeError:
            pass

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
    print('received: ' + url)
    prev = []
    
    # open the excel file
    excel = pd.ExcelFile('coinmarketcap.xlsx')

    # get the first sheet
    df = excel.parse(0)

    # find all mailto links
    for link in soup.find_all('a'):
        # get the href link
        # check if mailto
        try:
            if link.get('href').startswith('mailto:') and df['Email'].str.contains(link.get('href')).any() == False:
                print(link.get('href'))

                df.loc[len(df)] = [link.get('href')]

                print('In Excel')
            else:
                pass
        except AttributeError:
            pass

        # save the file
        df.to_excel('coinmarketcap.xlsx', sheet_name='Sheet1', index=False)




if __name__ == '__main__':
    main()
