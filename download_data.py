import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.simpletoolsforinvestors.eu/documentivari.php"

OUT_EOD = "data_end_of_day.csv"
OUT_INTRADAY = "data_intraday.csv"


def absolute_url(href: str) -> str:
    if href.startswith("http"):
        return href
    return f"https://www.simpletoolsforinvestors.eu/{href.lstrip('/')}"


def find_links():
    r = requests.get(BASE_URL)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    eod_link = None
    intraday_link = None

    # iterate over all table rows
    for row in soup.find_all("tr"):
        row_text = row.get_text(strip=True).lower()

        if "rendimenti e durate calcolati end of day" in row_text:
            a = row.find("a", href=True)
            if a:
                eod_link = absolute_url(a["href"])

        if "rendimenti e durate calcolati intraday" in row_text:
            a = row.find("a", href=True)
            if a:
                intraday_link = absolute_url(a["href"])

    return eod_link, intraday_link


def download(url: str, filename: str):
    r = requests.get(url)
    r.raise_for_status()
    with open(filename, "wb") as f:
        f.write(r.content)
    print(f"Saved {filename}")


def main():
    eod, intraday = find_links()

    if not eod or not intraday:
        raise RuntimeError("Could not find one or both download links")

    download(eod, OUT_EOD)
    download(intraday, OUT_INTRADAY)


if __name__ == "__main__":
    main()
