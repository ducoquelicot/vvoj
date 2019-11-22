'''

Script dat de website van de City Council van Palo Alto scrapet voor de agendas van 2019 en deze links opslaat in een CSV-bestand.
Let op: de agendas worden nu dus niet gedownload, we halen alleen de links van de site en slaan deze op. Hoe zou je ze kunnen downloaden?

OPDRACHT: Voeg een element toe aan het script zodat je alle links ook automatisch downloadt. 

'''

from bs4 import BeautifulSoup
import csv, fnmatch, os, requests, time, urllib.request

def main():
#   Main is ons basisscript. Hier definiëren we de dictiornary met urls die we willen gaan scrapen en lopen elke url na om er specifieke acties mee uit te voeren. 
#   We printen aan het einde van het script ook onze list met agendas, als controle.    
    pa_agenda = {2019: 'https://www.cityofpaloalto.org/gov/depts/cou/council_agendas.asp'}

    for year in pa_agenda.keys():
        output = scrape(pa_agenda[year])
        print(output)
        agendas = get_links(output)
#         writeout(agendas, year)

#         print(agendas)

def scrape(html_link):
#   Scrape is een functie die alle links van de url opslaat in een list.
    agenda = requests.get(html_link)
    soup = BeautifulSoup(agenda.text, 'html.parser')
    relevant_soup = soup.select('a')
    return relevant_soup

def get_links(links):
#   Get_links is een functie die aan de list met links de juist begin-url toevoegt indien nodig en deze toevoegt aan een list. 
    agendas = []
    for row in links:
        if row.getText()== 'Agenda and Packet':
            print(row)
            if fnmatch.fnmatch(row['href'], '*://www.cityofpaloalto.org/*'):
                agendas.append(row['href'])
                time.sleep(2)
            else:
                row['href'] = 'https://www.cityofpaloalto.org' + row['href']
                agendas.append(row['href'])
                time.sleep(2)
    return agendas

def writeout(agendas, years):
#   Writeout is een functie die de zojuist gemaakte list pakt en toevoegt aan een nieuwe csv.
    with open('ws_paloalto/agendas_{}.csv'.format(str(years)), 'w') as agenda:
        writer = csv.writer(agenda)
        writer.writerow(["Agenda and Packet"])
        for row in agendas:
            writer.writerow([row])

if __name__ == '__main__':
    main()