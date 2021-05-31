from scraper import Scraper

def main():
    scraper = Scraper()
    for category in scraper.categories:
        listings = scraper.scrapeCategory(category)
        scraper.writeToCsv(category, listings)

    # e.g. single category
    # listings = scraper.scrapeCategory('Computers, Parts and Supplies')
    # scraper.writeToCsv(Computers, Parts and Supplies, listings)

if __name__ == "__main__":
    main()