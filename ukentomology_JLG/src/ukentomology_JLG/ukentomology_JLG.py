import requests
from requests.exceptions import HTTPError
import json
import pandas as pd
import pyportal
from pyportal.constants import resources

def load_entData():
    """A dataframe of butterfly and moth museum specimens in the UK.

        This function allows users to access a dataframe containing
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
        load_ukentomology()
    """
    return pd.read_csv('data/ukentomology_data.csv', encoding='latin-1')


def entData_API(api_token):
    """Code allowing the user to re-access the LMNH and RAMM museum database
        APIs

        This function allows user to submit a get request to the LMNH and RAMM
        database APIs, and returns a cleaned and organized dataframe identical
        to that provided with the oackage.


        Parameters
        ----------
        api_token: str
            a personal api token obtained for the RAMM API

        
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
    """
    api_token = 'api_token'
    #Get request for the LMNH collection 
    lmnh_query = ('BMNH(E)+Lepidoptera')
    lmnh_params = {'resource_id':resources.specimens, 'q':lmnh_query} 
    lmnh_r = requests.get('http://data.nhm.ac.uk/api/3/action/datastore_search', params=lmnh_params)
    lmnh_r.status_code
    lmnh_json = lmnh_r.json()
    #Parsing json and creating dataframe
    lmnh_df = pd.DataFrame(lmnh_json['result']['records'])
    lmnh_df2['institution']='LMNH'
    lmnh_df3 = lmnh_df2.rename(columns={"_id": "id", "higherGeography":"countryOrigin", "year":"description"})
    lmnh_df3 = lmnh_df3[['institution', 'id', 'order', 'family', 'genus', 'scientificName', 'countryOrigin', 'description']]
    #Get request for the RAMM collection
    ramm_params = {'api_token':api_token, 
               'category':'natural-sciences', 
               'per_page':250}
    ramm_r = requests.get('https://api.swcollectionsexplorer.org.uk/api/v1/objects/', params=ramm_params)
    ramm_r.status_code
    #Parsing json and creating dataframe
    ramm_json = ramm_r.json()
    ramm_df = pd.DataFrame(ramm_json['data'])
    #Cleaning dataframe
    ramm_df['institution']='RAMM'
    ramm_df['order']='Lepidoptera'
    ramm_df['scientificName']=''
    ramm_df.loc[ramm_df["family"].isnull(),'family'] = ramm_df["full-name"]
    ramm_df2 = ramm_df[ramm_df['simple-name'].str.contains("butterfly|moth")]
    ramm_df2.loc[ramm_df2["scientificName"] == '','scientificName'] = ramm_df2["genus"] + ' ' + ramm_df2["species"]
    ramm_df3 = ramm_df2.rename(columns={"collection-country":"countryOrigin"})
    ramm_df3 = ramm_df3[['institution', 'id', 'order', 'family', 'genus', 'scientificName', 'countryOrigin', 'description']]
    #Concatenating dataframes
    frames = [lmnh_df3, ramm_df3]
    final_df = pd.concat(frames)
    return final_df

    
def entData_basic():
    """A function providing the shape of the dataframe, rows and columns, as well as a simple plot
        of the number of specimens present at each museum.
    """
    entData = pd.read_csv('~/Documents/GitHub/ukentomology_JLG/ukentomology_JLG/src/data/ukentomology_data.csv', encoding='latin-1')
    print ('The shape of this dataframe is ', entData.shape)
    print ('There are ', sum(entData.institution == 'LMNH'), ' specimens available at the LMNH')
    print ('There are ', sum(entData.institution == 'RAMM'), ' specimens available at the RAMM')
    ax = entData['institution'].value_counts().plot(kind='bar')
    ax.set_title("Museum Specimen Count")
    ax.set_xlabel("Institution Code")
    for p in ax.patches:
        ax.annotate("%.2f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    return ax

def entData_family():
    """A function providing the number of specimens in each family, as well as a bar plot for visualization.
    """
    print ('Number of specimens per family:', '\n', entData['family'].value_counts())
    ax = entData['family'].value_counts().plot(kind='bar')
    ax.set_title("Specimens Per Family")
    ax.set_xlabel("Family")
    return ax
