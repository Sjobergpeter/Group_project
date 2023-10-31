from flask import Flask, render_template
import requests
import random

from application import func

app= Flask(__name__)


@app.route("/")
def weather():
    # Hämtar data om användaren
    info = func.json_loads_on_uncorrected_list("http://ipinfo.io/json")

    # Hämtar koordinater från den datan om användaren
    lat = info["loc"].split(",")[0]
    lon = info["loc"].split(",")[1]

    # Ser regn och molntäcke på de koordinaterna
    weather = func.json_loads_on_uncorrected_list(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=rain,cloudcover&forecast_days=1")

    cloudcover = (weather['current']['cloudcover'])
    rain = (weather["current"]["rain"])

    # uppdaterar länken på knappen på hemsidan beroende på vädret
    link = None
    if rain != 0:
        link = "books"

    elif  rain == 0 and cloudcover < 40:
        link = "badplatser"

    else:
        link = "nästa aktivitet endpoint"

    
    return render_template("index.html", link=link)

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


@app.route("/books")
def books():

    # the app randomly chooses between swedish or english
    random_language = random.choice(["en", "sv"])
    
    # the app is reaching all books in the chosen language 
    api_url = f"https://gutendex.com/books?languages={random_language}"
    response = requests.get(api_url)

    # if the api is responsive
    if response.status_code == 200:

        #getting the full response from a webpage
        books = response.json()

        #we are extracting the amount of books in a certain language.
        book_amount = books.get('count')
        print(f"book amount: {book_amount}") #to delete later

        #we are choosing a random index 
        random_index = random.randint(1, book_amount-1)
        print(f"random_index: {random_index}") #to delete later

    
        '''there are 32 books on each page, so we are calculating what page to land on.
        this could be seen as an overkill, as we could have hard-coded the page numbers.
        but this makes the app more versitile - we could add more languages on the top of the page
        without having to change any code.'''
        page=random_index//32

        #accessing the new url
        if page == 0:
            api_url = f"https://gutendex.com/books?languages={random_language}"
        else:
            api_url = f"https://gutendex.com/books?languages={random_language}&page={page}"

        response = requests.get(api_url)
        books = response.json()

        #creating a random index
        random_number = random.randint(0, 31)

        #accessing a book of that index 
        random_book = books['results'][random_number]
        
        #getting the info about a book
        title = random_book['title']
        try:
            author = random_book['authors'][0]['name']
        except:
            author = "Unknown"
        downloads_number = random_book['download_count']
        read_link = random_book['formats']['text/html']
        cover = random_book['formats']['image/jpeg']

        
    else:
        title = "Boken misslyckades med att laddas!"

    return render_template('books.html', title=title, author=author, downloads_number=downloads_number, read_link=read_link, cover=cover)
  

if __name__ == "__main__":
    app.run(debug=True)

