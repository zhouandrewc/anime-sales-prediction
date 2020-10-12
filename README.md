# Metis Data Science Bootcamp Fall 2020 Project 2: Anime Sales Predictions

This repository contains the code, data, and documentation by Andrew Zhou.

## Problem Statement

Given data scraped from the Internet by our own means, we're tasked to employ linear regression to produce a model.

I chose to focus on predicting anime sales from various features. Our sales data were sourced from the [someanithing blog](https://www.someanithing.com/series-data-quick-view) and our anime series info were from [MyAnimeList](https://myanimelist.net/).

## Methods

Various regression and feature engineering techniques were attempted, including cross-validated linear, ridge, and lasso regression, forward subset selection, principal component analysis, and k-means clustering. Our principal feature engineering work was done in attempting to reduce the "genre" feature to a more manageable size and form.

### Tools Used

* BeautifulSoup
* pandas, numpy
* Matplotlib, Seaborn
* Scikit-learn, stats
* fuzzywuzzy ([installation instructions & guide](https://towardsdatascience.com/how-to-do-fuzzy-matching-in-python-pandas-dataframe-6ce3025834a6))

### Features Used

* MyAnimeList Score
* MyAnimeList Members
* Year
* Rating (PG, PG-13, R, etc.)
* Genres (binary variable indicating whether an anime belongs to a particular genre, almost 40 in total)

### Target Variable

* DVD sales of an anime show's first release, in millions of yen

## Contents

* [Data](data)

Various intermediate `.pickle` files produced by our scraping and cleaning process, as well as a final `anime_sales_df_v3.pickle` containing all of our required data for regression.

* [Utilities](utilities)

Utility functions to help with scraping, found in [`scraping_utilities.py`](utilities/scraping_utilities.py).

* [Notebooks](notebooks)

The code to clean and scrape our data, as well as to implement and evaluate our regressions. Notebooks are prefixed with the order of execution. Notebook 1 [scrapes sales data from someanithing](notebooks/1_scrape_anime_sales.ipynb); Notebook 2 [matches anime from the sales database to studios on MyAnimeList](notebooks/2_match_anime_to_studio.ipynb); Notebook 3 [matches the sales database anime to their MyAnimeList links and scrapes our desired features](notebooks/3_scrape_mal_anime_info.ipynb); Notebook 4 [does a final cleaning passthrough on the data](notebooks/4_final_clean.ipynb); and Notebook 5 [constructs, evaluates, and analyzes](notebooks/5_regression.ipynb) our linear regression model.

* [Presentation](presentation)

A [PDF](presentation/project_two_presentation_zhou_andrew.pdf) of the presentation given at bootcamp. Note that significant work was done and adjustments were made after the presentation was given and the current results are rather different, though much more reliable.

## Acknowledgments

Thanks to the awesome staff and students at Metis who were a huge help during this project.