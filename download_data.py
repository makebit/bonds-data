import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.simpletoolsforinvestors.eu/documentivari.php"

OUT_EOD = "data_end_of_day.csv"
OUT_INTRADAY = "data_intraday.csv"


def find_links():
    response = requests.get(BASE_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    eod_link = None
    intraday_link = None

    # New page layout:
    # Each download is contained in a Bootstrap .card.
    for card in soup.select(".card"):
        text = card.get_text(" ", strip=True).lower()

        if "rendimenti e durate calcolati end of day" in text:
            link = card.find("a", href=True)
            if link:
                eod_link = urljoin(BASE_URL, link["href"])

        elif "rendimenti e durate calcolati intraday" in text:
            link = card.find("a", href=True)
            if link:
                intraday_link = urljoin(BASE_URL, link["href"])

    return eod_link, intraday_link


def download(url, filename):
    response = requests.get(url, timeout=120)
    response.raise_for_status()

    with open(filename, "wb") as file:
        file.write(response.content)

    print(f"Saved: {filename}")


def main():
    eod, intraday = find_links()

    if not eod:
        raise RuntimeError("Could not find End of Day download link")

    if not intraday:
        raise RuntimeError("Could not find Intraday download link")

    print(f"EOD: {eod}")
    print(f"Intraday: {intraday}")

    download(eod, OUT_EOD)
    download(intraday, OUT_INTRADAY)


if __name__ == "__main__":
    main()
