import requests
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd


class HTMLScraper:
    '''
    A python based HTML Web Scraper using the requests module.
    '''

    def __init__(self):
        '''
        Base Class that implements utility functions like HTTP get requests.
        '''
        pass


    def log_error(self, e):
        """
        Placeholder to log messages.
        Currently using print(), but will replace it in future.
        """
        print(e)


    def verify_response_sanity(self, resp):
        """
        Returns True if the response seems to be HTML, False otherwise.
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)


    def fetch_html(self, url):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        """
        try:
            with closing(requests.get(url, stream=True)) as result:
                if self.verify_response_sanity(result):
                    return result.content
                else:
                    return None

        except RequestException as e:
            self.log_error(f'Error during requests to {url} : {str(e)}')
            return None


class IMDBWebScraper(HTMLScraper):
    '''
    A web crawler based on IMDB's box office collection HTML pages.

    Parameters
    ----------
    url : A valid url pointing to IMDB's box office collection page.

    Returns
    -------
    pd.DataFrame

    >>> parser = IMDBWebScraper()
    >>> for year in range(2010, 2019):
    >>>     print(parser.get_box_office_collection_by_year(year=str(year)).head())

    '''

    def __init__(self):
        '''
        Parse IMDB Box Office Collection Datasets.
        '''

        # This dict contains all features to store against the corresponding
        # key in the HTML attribute.
        self.tags_dict = {
            'rank'    : 'mojo-field-type-rank',
            'money'   : 'mojo-field-type-money',
            'name'    : 'mojo-field-type-release',
            'theaters': 'mojo-field-type-positive_integer',
            'date'    : 'mojo-field-type-date',
        }


    def get_box_office_collection_by_year(self, year = "2019"):
        """
        Parse data from the HTML page and return a pandas dataframe.
        """

        assert isinstance(year, str)
        assert len(year) > 0
        assert 2010 <= int(year) <= 2019

        box_office_url = f'https://www.boxofficemojo.com/year/{year}/?ref_=bo_yl_table_1'

        print("Fetching from " + box_office_url)
        response = self.fetch_html(box_office_url)

        # Check if the response is valid.
        if response is not None:
            html = BeautifulSoup(response, 'html.parser')
            movies = []

            # For each table-row in the HTML page.
            for tr in html.select('tr'):
                # Placeholder for each row in our dataframe.
                row = {
                    "rank"     : None,
                    "money"    : None,
                    "name"     : None,
                    "theaters" : None,
                    "date"     : None,
                }

                # Go through each child and look for the attribute to search.
                for child in tr.children:
                    for key in self.tags_dict.keys():
                        if self.tags_dict[key] in child.attrs['class']:
                            row[key] = child.text

                movies.append(row)

            movies = pd.DataFrame(movies)

            return movies

        # Raise an exception if we failed to get any data from the url
        raise Exception('Error retrieving contents at {}'.format(self.url))


# ------ GET BOX OFFICE COLLECTIONS ------
# parser = IMDBWebScraper()
# for year in range(2010, 2019):
#     print(parser.get_box_office_collection_by_year(year=str(year)).head())
