from scraper import Scraper
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()

    # parser.add_argument(action=..., nargs=..., const=..., default=..., type=..., choices=..., required=..., help=..., metavar=..., dest=..., version=...)
    parser.add_argument('--category', help="specify the name of a specific category to scrap from")
    args = parser.parse_args()
    scraper = Scraper()

    if args.category is None:
        for category in scraper.categories:
            listings = scraper.scrapeCategory(category)
            scraper.writeToCsv(category, listings)
    else:
        print(args.category)
        if args.category in scraper.categories:
            listings = scraper.scrapeCategory(args.category)
            scraper.writeToCsv(args.category, listings)
        else:
            # Computers, Parts and Supplies
            print("error: {} is not a valid category".format(args.category))

if __name__ == "__main__":
    main()