'''

Scraper die de website van het Vlaams Parlement scrapet voor de schriftelijke vragen tussen 1 oktober 2019 en 1 november 2019. Downloadt alle 
pagina's met de documentenfiche en slaat deze op op de lokale machine. 


'''

from bs4 import BeautifulSoup
import os, requests, time, urllib.request

def main():
#   main heeft alle url's en loopt deze vervolgens door het rijtje met wat ermee moet gebeuren.     
    urls = {}

    for page in range(0, 9):
        urls[page] = 'https://www.vlaamsparlement.be/parlementaire-documenten/zoekresultaten?query=&sort=date&initiatief%5B%5D=schriftelijke+vraag&publicatiedatum%5Bvan%5D%5Bdate%5D=01-10-2019&publicatiedatum%5Btot%5D%5Bdate%5D=01-11-2019&zittingsjaar=all&legislatuur=all&aggregatedstatus%5Btype%5D=none&aggregatedstatus%5Bvan%5D%5Bdate%5D=&aggregatedstatus%5Btot%5D%5Bdate%5D=&soort%5Bschv%5D=schv&vraagsteller=all&nummer=&volgnummer=&titel=&commissie=&page={}'.format(page)
        os.makedirs('ws_vlaams/scraped_urls', exist_ok=True)

    for link in urls.keys():
        output = scrape(urls[link])
        save_html(output)

def scrape(link):
#   scrape pakt alle links van de pagina's en zet die in een lijst
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    time.sleep(5)
    output = soup.select('a')
    return output

def save_html(output):
#   save_html slaat voor elke link in output de tekst op in een bestand dat op de lokale pc wordt gezet. 
    for row in output:
        if 'Bekijk de documentenfiche' in row.getText():
            row['href'] = 'https://www.vlaamsparlement.be{}'.format(row['href'])
            filename = row['href'][-7:]
            if not os.path.isfile('ws_vlaams/scraped_urls/{}.html'.format(filename)):
                urllib.request.urlretrieve(row['href'], 'ws_vlaams/scraped_urls/{}.html'.format(filename))
                time.sleep(2)
                print('File {} successfully saved.'.format(filename))

if __name__ == '__main__':
    main()