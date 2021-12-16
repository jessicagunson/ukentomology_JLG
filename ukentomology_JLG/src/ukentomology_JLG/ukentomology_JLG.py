import requests
from requests.exceptions import HTTPError
import json
import pandas as pd
import pyportal
from pyportal.constants import resources
import pkg_resources

def load_ukentomology():
    """A dataframe of butterfly and moth museum specimens in the UK.

        This package allows users to access a dataframe containing
        all butterfly and moth specimens preserved in entomology
        collections at the London Museum of Natural History (LMNH) and
        Royal Albert Memorial Museum (RAMM). 

        Contains the following columns:
        ------------------------------
        institution
            location of specimen; LMNH or RAMM
        id
            specimen ID number
        order
            scientific order
        family
            scientific family
        genus
            scientific genus
        scientificName
            the full scientific name of the specimen; genus and species
        countryOrigin
            the country in which the specimen was collected
        description
            notes regarding the specimen's collection, year collected, etc.

        

        Typical Usage Example
        ---------------------
    """
    return pd.read_csv('data/ukentomology_data.csv', encoding='latin-1')
