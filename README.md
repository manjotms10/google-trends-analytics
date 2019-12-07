# Google Trends Analytics
Course Project for UCSD ECE143: Programming for Data Analytics

## Proposal: What Google Trends Tell Us
This study is aimed at analyzing the Google Search trends and correlating them with real-world data. The main idea is to study what Google Search data tells us about the real world. For example, Google search trends can correlate well with the popularity of movies/video games. This correlation from various features will be analyzed and compared to observations from other available sources. <br>

## Dataset
- Google Trend data to be obtained by using Python API <br>
- Datasets from other sources, depending on specific topics. For example, the popularity of
a movie can be ascertained from its box office collection which can be scraped from IMDB or Metacritic websites. 
For video games, we make use of the VGChartz dataset <br>

## Repository Structure
conf - This directory contains the data files that were used/created during the process to store all our data <br>
---- movies - This subdirectory contains the data files for the analysis of movies <br>
---- video_games - This subdirectory contains the data files for the analysis of games <br>

src - This is the source directory containing all our code <br>
---- analytics - This package consists of the code that is used for creating, analyzing and plotting all the data <br>
-------- demo - This package contains the Jupyter notebook that showcases all our plots <br>
-------- movies - This package contains the web scraping and analysis code for movies topic <br>
-------- video_games - This package contains the data processsing and analysis code for video games topic <br>
---- utils - This is a common package that is used by both movies and video games for common processing. For e.g.,
		it consists of code for connecting to the GoogleTrends  API, obtaining visualizations and log info and errors <br>

## Code Demo:
- The Jupyter notebook is present under __src/analytics.demo__ package. The code makes use of PyTrends API to connect to Google 
Search data and returns a Pandas dataframe. This data is then compared to actual sales data obtained by scraping IMDB,
in the case of movies, and VGChartz dataset, in the case of video games. <br>
- All these visualizations can be obtained from the python files as well that are included in the __src/analytics.movies/analysis*.py files__ and __src/analytics.video_games/analysis*.py__ files. <br>
These script files can be run in the directory that contains them. <br>

## Third-party Modules
The following modules were used - <br>
beautifulsoup4-4.8.1, bs4-0.0.1, certifi-2019.9.11, chardet-3.0.4, cycler-0.10.0, idna-2.8, kiwisolver-1.1.0, lxml-4.4.1, matplotlib-3.1.1, numpy-1.17.4, pandas-0.25.3, pkg-resources-0.0.0, pyparsing-2.4.5, python-dateutil-2.8.1, pytrends-4.7.2, pytz-2019.3, requests-2.22.0, six-1.13.0, soupsieve-1.9.5, urllib3-1.25.7

## Contributors
Manjot Bilkhu (mbilkhu@ucsd.edu), Tushar Dobhal (tdobhal@ucsd.edu), Xiaolong He (xih251@ucsd.edu), 
Zhaoru Shang (z5shang@ucsd.edu), Terry Huang (t1huang@ucsd.edu)
