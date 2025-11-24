import unittest
from unittest.mock import patch, Mock
from web_scraper import WebScraper

class TestWebScraper(unittest.TestCase):

    @patch("requests.get")
    def test_grab_urls(self, mock_get):
        '''
        Mock a simple HTML page containing <b> and <a> tags; like the Tier 1
        liquidpedia page.
        Tests the scraper can parse the tournament pages from the link.
        '''

        html = """
        <html>
            <body>
                <b><a href="/fighters/Evolution_Championship_Series/2025/France/SF6" title="Evolution Championship Series/2025/France/SF6">Evolution Championship Series: France 2025</a></b>
                <b><a href="/fighters/Ultimate_Fighting_Arena/2023/SF6" title="Ultimate Fighting Arena/2023/SF6">Ultimate Fighting Arena 2023</a></b>
            </body>
        </html>
        """
        mock_response = Mock(status_code=200, text=html)
        mock_get.return_value = mock_response

        scraper = WebScraper()
        urls = scraper.grab_urls("https://liquipedia.net/x")

        expected = {
            "https://liquipedia.net/fighters/Evolution_Championship_Series/2025/France/SF6",
            "https://liquipedia.net/fighters/Ultimate_Fighting_Arena/2023/SF6"
        }

        self.assertEqual(set(urls), expected)

    @patch("requests.get")
    def test_grab_slugs(self, mock_get):
        '''
        Mock tournament pages that have different start.gg links.
        Tests whether the start.gg slugs can be pulled from the tournament links
        '''

        html_1 = """
        <html>
            <body>
                <a target="_blank" rel="nofollow noopener" class="external text" href="https://start.gg/tournament/evo-france-2025/event/street-fighter-6-ps5"><i class="lp-icon lp-start-gg"></i></a>
            </body>
        </html>
        """
        html_2 = """
        <html>
            <body>
                <a target="_blank" rel="nofollow noopener" class="external text" href="https://start.gg/tournament/ultimate-fighting-arena-2023/event/street-fighter-6"><i class="lp-icon lp-start-gg"></i></a>
            </body>
        </html>
        """
        html_3 = ''  # simulate a page with no start.gg link

        mock_get.side_effect = [
            Mock(status_code=200, text=html_1),
            Mock(status_code=200, text=html_2),
            Mock(status_code=200, text=html_3)
        ]

        scraper = WebScraper()
        url_list = ["url1", "url2", "url3"]

        result = list(scraper.grab_slugs(url_list))  # convert zip to list for testing

        expected = [
            ("url1", "evo-france-2025"),
            ("url2", "ultimate-fighting-arena-2023"),
            ("url3", None)
        ]

        assert result == expected