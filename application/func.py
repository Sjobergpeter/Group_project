# Importera pythons urllib för att göra anrop på extern API, importera ssl, json
import urllib.request
import ssl
import json
import pandas as pd



def json_loads_on_uncorrected_list(data_url):
    """Funktion för att omvandla json data från API till python."""

    ## Uppkopplingen mot API:et behöver inte vara krypterat.
    context = ssl._create_unverified_context()

    json_data = urllib.request.urlopen(data_url, context=context).read()

    ## Gör om json till en dictionary som är fullt läsbar med Python
    data = json.loads(json_data)

    ## Returnerar python dict.
    return data

'''Functions for books'''

'''The function builds a dataframe, extracting columns title, authors, and subjects.
It then displays it as a html table.'''
def build_df(books):

    df = pd.DataFrame(books['results'], columns=['title', 'authors', 'subjects'])
    
    # If the df is empty the program displays a custom message
    if df.empty:

        data = "Försök igen med ett annat ord! Ingenting hittades."
        return data
    
    # If there is the  data in dataframe, the function formats it and returns it as a html table
    else:

        df['authors'] = df['authors'].apply(lambda author_list: author_list[0]['name'] if author_list and len(author_list) > 0 else 'Okänd')
        df['subjects'] = df['subjects'].apply(lambda subjects_list: ' / '.join(subjects_list) if subjects_list else 'Okänd')
        
        data=df.to_html()
        return data