from bs4 import BeautifulSoup
import requests
import re
import json
import unicodecsv as csv
import os
import datetime
import errno

class Scraper:
    def __init__(self):
        self.categories = self.get_categories()

    def get_categories(self):
        url = 'https://govdeals.com'
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        categories = soup.find('div', id='categories')
        links = categories.find_all('a', id='cat_link')
        badges = categories.find_all('span', class_='badge')

        counts = list(map(lambda x : x.text, badges))

        output = dict()
        for idx, link in enumerate(links):
            code = link['href'].split("mycat=")[-1]
            text = link.text
            output[text] = {
                'code': code,
                'count': counts[idx]
            }

        return output

    def get_listings(self, catCode, count):
        # example URL:
        # 'https://www.govdeals.com/index.cfm?fa=&searchPg=Category&additionalParams=true&sortOption=ad&timing=BySimple&timingType=&category=62'
        url = 'https://govdeals.com/index.cfm'
        payload = {
            'fa': 'Main.AdvSearchResultsNew',
            'searchPg': 'Category',
            'additionalParams': 'true',
            'sortOption': 'ad',
            'timing': 'BySimple',
            'timingType': '',
            'category': catCode,
            'StartRow': 1,
            'rowCount': count
        }
        soup = BeautifulSoup(requests.get(url, params=payload).text, 'lxml')
        container = soup.find('div', id='container_srch_results')
        rows = container.find_all('div', id='boxx_row')

        output = list()
        for row in rows:
            location = list()
            numBids = 0
            date = "ERROR"
            bid = 0

            try:
                divs = row.find_all('div', recursive=False)
                date = divs[3].label.contents
                date[0] = date[0].split(' ')[0]
                date[1] = date[1].text
                bid = divs[4].find('span', id='bid_price').contents
                
                if len(bid) == 3:
                    numBids = bid[-1].split("Bids:")[1].strip()

                for item in divs[2].contents[2:]:
                    item = str(item).strip()
                    if item != '<br/>':
                        location.append(item)
            except Exception as e:
                print(e)
                print(numBids)

            output.append({
                'photo': 'https://govdeals.com{}'.format(divs[0].a['href']),
                'href': 'https://govdeals.com/{}'.format(divs[1].a['href']),
                'description': divs[1].a.text,
                'location': " ".join(location).strip(),
                'auctionClose': "{} {}".format(date[0], date[1]),
                'bid': bid[0].strip(),
                'numBids': numBids
            })

        return output

    def scrapeCategory(self, category):
        print("Scraping ", category)
        catCode = self.categories[category]['code']
        count = self.categories[category]['count']
        return self.get_listings(catCode, count)
        # print(json.dumps(listings, indent=4))

    def writeToCsv(self, filename, data):
        columns = ["description", "bid", "numBids", "auctionClose", "location", "href", "photo"]
        filename = str(filename).strip().replace(' ', '_')
        filename = re.sub(r'(?u)[^-\w.]', '', filename)

        my_dir = os.path.join(
            os.getcwd(), 
            "output",
            filename
        )

        try:
            os.makedirs(my_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("error creating directory")
                return

        try:
            dt = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            f = os.path.join(my_dir, "{}.csv".format(dt))
            print("Creating file: {}".format(f))
            with open(f, 'wb+') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
                for datum in data:
                    writer.writerow(datum)
        except IOError as e:
            print("error occurred while writing to file")
            print(e)                

        