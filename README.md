# Google Trends Analytics
Course Project for UCSD ECE143: Programming for Data Analytics

## Proposal: What Google Trends Tell Us

Problem: <br>
This study is aimed at analyzing the Google Search trends and correlating them with real-world
data via predictive analysis. The main idea is to study what Google Search data tells us about the
real world and then develop models to predict the outcome of an event. For example, Google
search trends can correlate well with the popularity of movies/video games. This correlation from various 
features will be analyzed and compared to observations from other available sources. <br>

## Dataset:
- Google Trend data to be obtained by using Python API <br>
- Datasets from other sources, depending on specific topics. For example, the popularity of
a movie can be ascertained from its box office collection which can be scraped from the
internet. <br>

## Project Structure:
conf - This directory contains the data files that were used/created during the process to store all our data <br>
---- movies - This subdirectory contains the data files for the analysis of movies <br>
---- video_games - This subdirectory contains the data files for the analysis of games <br> <br>

src - This is the source directory containing all our code <br>
---- analytics - This package consists of the code that is used for creating, analyzing and plotting all the data <br>
-------- demo - This package contains the Jupyter notebook that showcases all our plots <br>
-------- movies - This package contains the web scraping and analysis code for movies topic <br>
-------- video_games - This package contains the data processsing and analysis code for video games topic <br>
---- utils - This is a common package that is used by both movies and video games for common processing. For e.g.,
			 it consists of code for connecting to the GoogleTrends  API, obtain visualizations and log info and errors <br>

## Code Demo:
The Jupyter notebook is present under src/analytics.demo package. The code makes use of PyTrends API to connect to Google 
Search data and returns a Pandas dataframe. This data is then compared to actual sales data obtained by scraping IMDB,
in the case of movies, and VGChartz dataset, in the case of video games. All these visualizations can be obtained from 
the python files as well that are included in the src/analytics.movies/analysis*.py files and 
src/analytics.video_games/analysis*.py files 

## Contributors
Manjot Bilkhu (mbilkhu@ucsd.edu), Tushar Dobhal (tdobhal@ucsd.edu), Xiaolong He (xih251@ucsd.edu), 
Zhaoru Shang (z5shang@ucsd.edu), Terry Huang (t1huang@ucsd.edu)
