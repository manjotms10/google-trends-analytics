import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

sys.path.append("../../")
from utils.google_trends import GoogleTrends
from data_utils import IMDBWebScraper


def box_office_by_year(query_year, google_trends, imdb_parser, path):
    '''
    Plot Box Office Collections vs Google Trends by year.

    Parameters
    ----------
    query_year:    A valid year between 2010 and 2019, passed as a string.
    google_trends: A valid instance of GoogleTrends class.
    imdb_parsed:   A valid instance of IMDBWebScraper class.
    path:          A valid path to save the resultant plot.

    Returns
    -------
    None

    Example:
    >>> google_trends = GoogleTrends()
    >>> imdb_parser = IMDBWebScraper()
    >>> path = "../../../plots/movies/"
    >>> box_office_by_year("2019", google_trends, imdb_parser, path)
    '''

    assert isinstance(query_year, str)
    assert len(query_year) == 4
    assert 2010 <= int(query_year) <= 2019

    # Get the result from box office collection parser.
    box_office_df  = imdb_parser.get_box_office_collection_by_year(query_year)
    idx            = np.random.choice(range(box_office_df.shape[0]), 15)
    movies         = list(box_office_df.iloc[idx]["name"])
    start_date     = query_year + "-01-01"
    end_date       = query_year + "-12-31"

    # Query pytrends
    google_trends_box_office_df = \
            google_trends.get_trends_data_from_multiple_keywords(
                                        keywords = movies,
                                        start_date = start_date,
                                        end_date = end_date).data

    # Sum all the queries across the year.
    total_queries = google_trends_box_office_df.sum(axis = 0)

    # Parse result from Box Office Collections (str).
    box_office_collections = list(box_office_df.iloc[idx]["money"])
    for i in range(len(box_office_collections)):
        box_office_collections[i] = \
                ''.join(box_office_collections[i][1:].split(','))

    data = []
    for movie, val in zip(movies, box_office_collections):
        data.append((int(total_queries[movie]), int(val)))

    # Create a dataframe to hold results and compare.
    df = pd.DataFrame(data, columns = ["pytrends", "imdb"], index=movies)
    
    # Normalize the columns
    cols_to_norm     = ['pytrends','imdb']
    df[cols_to_norm] = df[cols_to_norm].apply(
                            lambda x: (x - x.min()) / (x.max() - x.min()))

    # ------ View Plot ------
    # ax = df.plot.bar(rot=0)
    # plt.show()

    # Plot the comparison and save the result.
    fig = df.plot.bar(rot=0, figsize=(50,15)).get_figure()
    fig.savefig(path + f'{query_year}_plot_{str(np.random.randint(1, 10))}.png')


if __name__ == '__main__':
    # Create data loaders for Google Trends and IMDBWebScraper
    google_trends   = GoogleTrends()
    imdb_parser     = IMDBWebScraper()
    path            = ""

    for year in range(2010, 2019):
        #try:
        box_office_by_year(str(year), google_trends, imdb_parser, path)
        # except:
        #     print("Exception occured with year = ", year, "\n")
