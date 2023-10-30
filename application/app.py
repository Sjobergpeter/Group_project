from flask import Flask

app= Flask(__name__)


# Endpoint för badplatser
@app.route("/badplatser")
def beaches_in_Sthml():
    """Visar lista på badplatser i Stockholm med tillhörande koordinater"""

    ## Inhämtar data om badplater från extern API
    data_url = f"https://apigw.stockholm.se/api/PublicHittaCMS/api/serviceunits?&filter[servicetype.id]=104&page[limit]=1500&page[offset]=0&sort=name"

    ## Anropar funktionen som konverterar json data till python och sparar i variabel.
    beach_list=func.json_loads_on_uncorrected_list(data_url)

    ## Lista på badplatser med unicode och badplatsen koordinater
    beach_info = []

    for b in beach_list["data"]:
        beach_name_unicode=b["attributes"]["name"]
        beach_coordinate=b["attributes"]["location"]
        beach_info.append({"name": beach_name, "location": beach_coordinate})

    return beach_info

if __name__ == "__main__":
    app.run(debug=True)

