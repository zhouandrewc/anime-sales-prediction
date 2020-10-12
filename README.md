# Metis Data Science Bootcamp Fall 2020 Project 2: Anime Sales Predictions

This repository contains the code, data, and documentation by Andrew Zhou.

Documentation is sparse at the moment but will be updated ASAP.

## Problem Statement

Given data scraped from the Internet by our own means, we're tasked to employ linear regression to produce a model.

I chose to focus on predicting anime sales from various features. Our sales data were sourced from the [someanithing blog](https://www.someanithing.com/series-data-quick-view) and our anime series info were from [MyAnimeList](https://myanimelist.net/).

## Methods

Various regression and feature engineering techniques were attempted, including cross-validated linear, ridge, and lasso regression, forward subset selection, principal component analysis, and k-means clustering. Our principal feature engineering work was done in attempting to reduce the "genre" feature to a more manageable size and form.

## Contents

* [Data](data)

Various intermediate `.pickle` files produced by our scraping and cleaning process, as well as a final `anime_sales_df_v3.pickle` containing all of our required data for regression.

* [Code](notebooks)

The code to clean and scrape our data, as well as to implement and evaluate our regressions.

* [Presentation](presentation)

A PDF of the presentation given at bootcamp. Note that significant work was done and adjustments were made after the presentation was given and the current results are rather different, though much more reliable.

## Acknowledgments

Thanks to the awesome staff and students at Metis who were a huge help during this project.