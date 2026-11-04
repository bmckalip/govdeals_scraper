# GovDeals Scraper

A historical Python research prototype that reads GovDeals auction categories and exports listing information to CSV.

## Status

The scraper was written against the site's HTML structure in 2021. Its selectors and live-site behavior have not been revalidated. The repository currently has no pinned dependency file or license file.

## Setup

Create and activate a Python 3 virtual environment, then install the libraries imported by the scraper:

```sh
python -m pip install beautifulsoup4 requests unicodecsv lxml
```

## Usage

From the repository root, view the command options:

```sh
python src/driver.py --help
```

To request a category, pass its exact name as it appears in the categories returned by the site:

```sh
python src/driver.py --category "<exact category name>"
```

Omitting `--category` processes every category discovered on the home page. Category discovery happens when `Scraper()` is created, so normal execution requires network access and compatible site markup. The `--help` path exits before creating the scraper.

## Output

The scraper writes timestamped files under `output/<category>/<YYYY-MM-DD_HH-MM-SS>.csv`, relative to the working directory. Columns are:

- `description`
- `bid`
- `numBids`
- `auctionClose`
- `location`
- `href`
- `photo`

## Source layout

- [src/driver.py](src/driver.py): command-line arguments and category selection.
- [src/scraper.py](src/scraper.py): HTML requests, parsing and CSV output.

This housekeeping pass documents the existing implementation; it does not claim a current live scraping result.
