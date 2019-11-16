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

    Example:
    >>> parser = IMDBWebScraper()
    >>> box_office_df = parser.get_box_office_collection_by_year(year="2019")
    >>> top_50_action = parser.get_top_movies_by_genre(genre="action", metric="num_votes")

    '''

    def __init__(self):
        '''
        Parse IMDB Box Office Collection Datasets.
        '''

        self.genres  = ["action", "comedy", "Horror", "Sci-Fi", "Drama", "Romance"]
        self.metrics = ["boxoffice_gross_us", "num_votes"]

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

        box_office_url = 'https://www.boxofficemojo.com/year/' +\
                         f'{year}/?ref_=bo_yl_table_1'

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
        raise Exception('Error retrieving contents at {}'.format(box_office_url))


    def get_top_movies_by_genre(self, genre = "action", metric = "num_votes"):
        """
        Parse HTML data from IMDB Top 50 page and return a pandas DataFrame.
        """

        assert isinstance(genre,  str)
        assert isinstance(metric, str)

        assert genre  in self.genres
        assert metric in self.metrics

        imdb_url = 'http://www.imdb.com/search/title/?title_type=movie' + \
                   f'&genres={genre}&sort={metric},desc' + \
                   '&explore=title_type,genres'

        response = self.fetch_html(imdb_url)

        # Check if the response is valid.
        if response is not None:
            html = BeautifulSoup(response, 'html.parser')

            # For each movie in the HTML page.
            movies = html.findAll("div", {"class": "lister-item mode-advanced"})
            result = []

            for movie in movies:
                rank  = movie.find("span").text.split('.')[0]
                name  = movie.find("h3").find("a").text
                year  = movie.find("span", {
                                    "class": "lister-item-year text-muted unbold"
                                }).text[1:-1]
                if len(year) > 4:
                    year = year[-4:]
                span  = movie.find("p", {"class": "sort-num_votes-visible"})\
                             .findAll("span", {"name": "nv"})

                assert len(span) >= 1, "Could Not find Votes and Gross"
                votes = span[0].text
                if len(span) > 1:
                    gross = span[1].text[1:-1]
                else:
                    gross = "0"

                result.append({
                    "rank"  : rank,
                    "name"  : name,
                    "year"  : year,
                    "votes" : votes,
                    "gross" : gross,
                })

            return pd.DataFrame(result)

        # Raise an exception if we failed to get any data from the url
        raise Exception('Error retrieving contents at {}'.format(imdb_url))
