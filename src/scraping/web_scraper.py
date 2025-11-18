import requests, os, time
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class WebScraper():
    '''
    Class used for scraping liquidpedia tournament pages for sf6.

    Methods
    -------
    grab_urls(url=str)
        Takes a string URL for a liquidpedia page that contains tournament
        links and returns a list of liquidpedia tournament pages.
    
    grab_slugs(url_list=list)
        Takes a list of liquidpedia tournament links and parses them for 
        start.gg links, then returns a zip that contains tuples consisting of
        the url and the associated start.gg slug. Slug can be None. 
    
    write_to_csv(zipped=zip, out=str)
        Takes a zip object and output string, and writes the zip object to a csv
        file with name "out".
    '''

    def __init__(self):
        pass

    def grab_urls(self, url: str):
        try:
            headers={"User-Agent": "Mozilla/5.0"}
            for _ in range(1):
                response = requests.get(url, headers=headers)
                if response.status_code != 429:
                    break
                time.sleep(1)

            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            print(f"Request failed, likely rate limit: {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            return []

        tournament_links = []

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Scanning URL for tournament pages...")

        # all tourney page links are stored in <a> tags within <b> tags
        soup = BeautifulSoup()
        bold_tags = soup.find_all("b")
        for b_tag in tqdm(bold_tags, desc="Progress", unit="tag"):
            a_tag = b_tag.find("a")
            if a_tag and a_tag.get("href"):
                href = a_tag["href"]

                # found tag only contains redirect: so we add domain
                full_url = urljoin("https://liquipedia.net", href)
                tournament_links.append(full_url)

        tournament_links = list(set(tournament_links))
        print(f"Found {len(tournament_links)} tournament pages:")

        return tournament_links

    def grab_slugs(self, url_list: list):
        slug_list = []

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Scanning URL list for start.gg links...")

        for url in tqdm(url_list, desc="Progress", unit="url"):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.select("a.external.text")
            slug_found = False

            for a in links:
                href = a.get("href", "")

                if "start.gg" in href:
                    parsed = urlparse(href)
                    path_parts = parsed.path.strip("/").split("/")

                    # start.gg links always have the same format, with the slug
                    #   after "tournament/"
                    try:
                        slug_index = path_parts.index("tournament")+1
                        slug_list.append(path_parts[slug_index])
                        slug_found = True
                        break

                    except ValueError:
                        pass

            if not slug_found:
                slug_list.append(None)

        none_count = sum(1 for _ in slug_list if _ is None)
        print(f"Number of Liquidpedia pages without a Start.gg slug: {none_count}")

        return zip(url_list, slug_list)

    def write_to_csv(self, zipped: zip, out: str):
        pass

if __name__ == "__main__":
    # test = WebScraper()
    # l = test.grab_urls("https://liquipedia.net/fighters/Street_Fighter_6/Tier_2_Tournaments")
    # test.grab_slugs(l)
    pass