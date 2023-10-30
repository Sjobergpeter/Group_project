# Importera pythons urllib för att göra anrop på extern API, importera ssl, json
import urllib.request
import ssl
import json


def correct_unicode(string):
    """Funktion för att ändra unicode till svenska specialtecken"""

    ## Ändra unicode till svenska bokstäver.
    corrected_name = string.encode('latin-1').decode('unicode_escape')

    ## Returnerar korrigerat namn
    return corrected_name


def json_loads_on_uncorrected_list(data_url):
    """Funktion för att omvandla json data från API till python."""

    ## Uppkopplingen mot API:et behöver inte vara krypterat.
    context = ssl._create_unverified_context()

    json_data = urllib.request.urlopen(data_url, context=context).read()

    ## Gör om json till en dictionary som är fullt läsbar med Python
    data = json.loads(json_data)

    ## Returnerar python dict.
    return data