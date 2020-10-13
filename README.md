# Metis Data Science Bootcamp Fall 2020 Project 2: Anime Sales Predictions

This repository contains code, data, and documentation for Andrew Zhou's Anime Sales Predictions project for the Metis Data Science Bootcamp.

## Problem Statement

Given data scraped from the Internet by our own means, we're tasked to employ linear regression to produce a model.

I chose to focus on predicting anime sales, as measured by the sales of the first release of anime DVDs, from various features. The importance of these sales, though perhaps overstated at times, still far outstrips the importance of DVD sales in the U.S., and is considered one metric to measure the success of an anime, as [various](https://www.animenewsnetwork.com/feature/2012-03-07) [sources](https://www.someanithing.com/sales-faqguide) attest.

Our sales data were sourced from the [someanithing blog](https://www.someanithing.com/series-data-quick-view) and our anime series info were from [MyAnimeList](https://myanimelist.net/).

## Methods

Various regression and feature engineering techniques were attempted, including cross-validated linear, ridge, and lasso regression, forward subset selection, principal component analysis, and k-means clustering. Our principal feature engineering work was done in attempting to reduce the "genre" feature to a more manageable size and form.

### Tools Used

* BeautifulSoup
* pandas, numpy
* Matplotlib, Seaborn
* Scikit-learn, stats
* fuzzywuzzy ([installation instructions & guide](https://towardsdatascience.com/how-to-do-fuzzy-matching-in-python-pandas-dataframe-6ce3025834a6))

### Techniques Used

* Regression Methods
    * Ordinary Least Squares Regression
    * Polynomial Regression
    * Ridge Regression
    * Lasso Regression
* Feature Engineering
    * Forward Selection (Features)
    * Principal Component Reduction
    * k-means Clustering
    * Kruskal-Wallis Statistical Test

### Features Used

* MyAnimeList Score
* MyAnimeList Members
* Year
    * 2000 to 2020
* Rating
    * PG, PG-13, R, etc.
* Source
    * e.g. Manga, Original, Light Novel
* Genres
    * Binary Variables, 40 in total
    * 1 if anime belongs to the genre, 0 otherwise
    * e.g. Action, Comedy, Drama

### Target Variable

* DVD sales of an anime show's first release, in millions of yen

## Contents

* [Data](data)

Various intermediate `.pickle` files produced by our scraping and cleaning process, as well as a final `anime_sales_df_final.pickle` containing all of our required data for regression.

* [Utilities](utilities)

Utility functions to help with scraping, found in [`scraping_utilities.py`](utilities/scraping_utilities.py).

* [Notebooks](notebooks)

The code to clean and scrape our data, as well as to implement and evaluate our regressions. Notebooks are prefixed with the order of execution. [Notebook 1](notebooks/1_scrape_anime_sales.ipynb) scrapes sales data from someanithing; [Notebook 2](notebooks/2_match_anime_to_studio.ipynb) matches anime from the sales database to studios on MyAnimeList; [Notebook 3](notebooks/3_scrape_mal_anime_info.ipynb) matches the sales database anime to their MyAnimeList links and scrapes our desired features; [Notebook 4](notebooks/4_final_clean.ipynb) does a final cleaning passthrough on the data; and [Notebook 5](notebooks/5_regression.ipynb) constructs, evaluates, and analyzes our linear regression model.

* [Presentation](presentation)

A [PDF](presentation/project_two_presentation_zhou_andrew.pdf) of the presentation given at bootcamp. Note that significant work was done and adjustments were made after the presentation was given and the current results are rather different, though much more reliable.

## Limitations and Further Work

Our project mostly functions as proof of concept rather than as a decision-making or prognosticating tool; it cannot be used to predict whether an anime will succeed before it airs. Certain features used are unlikely to be available when an anime is unreleased, and others develop, accumulate, and change over time. Additionally, the data are from Western sources and so may lack predictivity compared to comparable Japanese data. Improvements to the model might include tracking time series data, analyzing trends, and more generally acknowledging the time-dependent nature of our features.

## Acknowledgments

Thanks to the awesome staff and students at Metis who were a huge help during this project.