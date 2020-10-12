"""
Utilities module containing functions to scrape anime sales information
from https://www.someanithing.com/series-data-quick-view and
https://myanimelist.net/. In documentation we refer to MyAnimeList as MAL.

Due to the issue of matching names of anime and studios from the two sites,
we will refer to SAT versus MAL names and titles.

@author Andrew Zhou
@updated Oct 12 2020
"""

from bs4 import BeautifulSoup
import requests
import re
import string
import time
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

def get_soup(url):
    """
    Given a url, returns a BeautifulSoup object representing the parsed page

    :param str url: the url of the site to scrape

    :return: BeautifulSoup object for the page
    :rtype: bs4.BeautifulSoup
    """
    page = requests.get(url).text
    return BeautifulSoup(page, "lxml")

def get_anime_of_studio(studio_url):
    """
    Given the url of an anime studio's MAL page, grabs the MAL titles
    and links of all the anime associated with that studio.

    :param str studio_url: The base URL for a studio on MAL, e.g.
        https://myanimelist.net/anime/producer/7/JCStaff. Formatted as
        https://myanimelist.net/anime/producer/%studio_index/%studio_name
        where index is some integer and studio_name is the (possibly modified)
        studio name.

    :return: A dictionary representing all the anime on the studio's page.
        The keys are MAL anime names and the values are the corresponding MAL
        anime links.
    :rtype: dict of str: str
    """
    anime_titles = []
    anime_links = []

    # Each studio has a number of pages of anime titles. We will iterate over
    # pages until we detect that we've exhausted them.
    page_num = 1
    while True:
        time.sleep(2)

        page_url = studio_url + "?page=" + str(page_num)
        soup = BeautifulSoup(requests.get(page_url).text, "lxml")

        anime_els = soup.find_all("h2", class_="h2_anime_title")

        if anime_els:
            anime_titles += list(map(lambda x: str(x.string), anime_els))
            anime_links += list(el.a["href"] for el in anime_els)
        else:
            # If we don't find any elements, we've scraped all the pages and
            # we can end the loop
            break

        page_num += 1

    return dict(zip(anime_titles, anime_links))

def get_mal_studio_info():
    """
    Get a list of all studios on MAL.

    :return studio_dict: A dictionary representing all the the studios listed
        on MAL. The keys are MAL studio names and the values are the
        corresponding MAL studio links.
    :rtype: dict of str: str
    """

    # The url of the list of studios represented on MAL (the "producer" list
    # includes studios)
    studios_url = "https://myanimelist.net/anime/producer"
    soup = get_soup(studios_url)

    studio_els = soup.find_all("a", href=re.compile(r"/anime/producer/"))

    studio_dict = {}
    for el in studio_els:
        studio_name = re.match(r"(.*) \(\d+\)", el.get_text()).group(1).strip()
        studio_link = "https://myanimelist.net" + el.attrs["href"]
        studio_dict[studio_name] = studio_link
    #studio_names = [re.match(r"(.*) \(\d+\)", el.get_text()).group(1).strip() for el in studio_els]
    #studio_links = ["https://myanimelist.net" + el.attrs["href"] for el in studio_els]

    return studio_dict

def studio_name_matcher(sales_studio_names, mal_studio_names):
    """
    Match SAT studio names to MAL studio names by removing whitespace and
    punctuation and ignoring case. Some manual adjustments are also needed,
    and are performed in a Jupyter notebook.

    :param list of str sales_studio_names: a list of all SAT studio names
    :param list of str mal_studio_names: a list of all MAL studio names

    :return matcher: A dictionary to help match SAT studio names to MAL
        studio names. The keys are SAT studio names and the values are the
        corresponding MAL studio names.
    :rtype: dict of str: str
    """
    translator = str.maketrans('', '', string.punctuation + ' ')

    """
    Modify a studio name to simplify matching.

    :param str name: A studio name
    :return: The formatted studio name
    :rtype str:
    """
    def find_mod_name(name):
        return name.lower().translate(translator)

    matcher = {}

    mal_studio_mod_names = list(map(find_mod_name, mal_studio_names))

    for name in sales_studio_names:
        mod_name = find_mod_name(name)
        match_idx = mal_studio_mod_names.index(mod_name)

        try:
            matcher[name] = mal_studio_names[match_idx]
        except:
            print("Exception: Studio name unmatched")
            print("Studio name:", name)

    return matcher

def create_studio_df(mal_studio_info, matched_studio_names):
    """
    Create a DataFrame with all of our studio information. Index is the MAL
    studio name, columns are "link" (its MAL url) and "anime_info", a dict
    where keys are the studio's anime names and values are their MAL links.

    :param dict of str: str mal_studio_info:
        A dictionary representing all the the studios listed
        on MAL. The keys are MAL studio names and the values are the
        corresponding MAL studio links.
    :param list of str matched_studio_names: a list of all MAL studio names
        corresponding to a studio in our sales data; we ignore all other
        studios

    :return pd.DataFrame studio_df: a DataFrame indexed by all matched studios
        :index of str: The names of all matched studios
        :columns:
            :column of str studio_link: the MAL url for the studio page
            :dict of str: str anime_info: a dict where the keys are the anime
                names for that particular studio, and the values are the links
                to the MAL pages for those anime
    :rtype: pd.DataFrame
    """

    studio_df = pd.DataFrame(columns=["link", "anime_info"])

    for studio_name, studio_link in mal_studio_info.items():
        if studio_name in matched_studio_names:
            print(studio_name)
            try:
                anime_info = get_anime_of_studio(studio_link)
            except:
                print("Exception in getting anime information. Returning \
                       incomplete dataframe early. Potentially a connection \
                       issue.")
            studio_row = pd.Series(data=[studio_link, anime_info],
                                   index=["link", "anime_info"],
                                   name=studio_name)
            studio_df = studio_df.append(studio_row)

    return studio_df


def get_anime_link(sales_anime_name, studio_anime_info, fuzzy_match=False, ratio=None):
    """
    Given the name of an anime from the sales data source and MAL information
    on all the anime its studio has produced, attempts to match the anime to
    an MAL link.

    Uses fuzzy matching and may match erroneously if the ratio is too low.
    Fuzzy matches may need to be inspected afterwards.

    :param str sales_anime_name: the name of an anime from the sales data
    :param dict str: str studio_anime_info: a dict where the keys are the MAL
        anime names for that particular studio, and the values are the links
        to the MAL pages for those anime
    :param bool fuzzy_match: whether to use fuzzy matching
    :param ratio: a number from 0 to 100 indicating the threshold over which
        to fuzzy match. 100 requires a perfect match (aside from case).
    """
    studio_anime_names = list(studio_anime_info.keys())
    studio_anime_links = list(studio_anime_info.values())

    ratios = list(map(lambda x: fuzz.ratio(sales_anime_name.lower(), \
                                           x.lower()), studio_anime_names))

    max_index = np.argmax(ratios)
    if ratios[max_index] > ratio:
        return studio_anime_links[max_index]
    return None
