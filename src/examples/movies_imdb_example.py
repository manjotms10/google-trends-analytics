import sys
sys.path.append("../")

from analytics.movies.data_utils import IMDBWebScraper
import pandas as pd

# ------ GET BOX OFFICE COLLECTIONS ------
parser = IMDBWebScraper()
for year in range(2010, 2019):
    print("Box Office Collections for the year: ", year)
    print(parser.get_box_office_collection_by_year(year=str(year)).head(10))
    print("\n")

# ------ GET IMDB TOP 50 DATA ------
parser = IMDBWebScraper()
for genre in ["action", "comedy", "Horror", "Sci-Fi", "Drama", "Romance"]:
    for metric in ["boxoffice_gross_us", "num_votes"]:
        try:
            df = parser.get_top_movies_by_genre(genre=genre, metric=metric).head(10)
            print("Top 10 ", genre, " movies based on ", metric)
            print(df.head(10))
            print("\n")
        except AssertionError:
            print("Assertion Hit at ", genre)
