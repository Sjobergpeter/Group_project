from flask import Flask, render_template, request
import requests
import random
from . import func
from application import func
import pandas as pd

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
    weather = func.json_loads_on_uncorrected_list(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude=[{lon}&current=rain,snowfall,cloudcover")

    cloudcover = (weather['current']['cloudcover'])
    rain = (weather["current"]["rain"])
    snowfall = (weather["current"]["snowfall"])

    # uppdaterar länken på knappen på hemsidan beroende på vädret
    link = None
    if rain != 0:
        link = "books"

    elif  rain == 0 and cloudcover < 40:
        link = "badplatser"

    elif snowfall > 0:
        link = "movie"
    
    else:
        link = "anything"

    
    return render_template("index.html", link=link)

# Endpoint för badplatser
@app.route("/badplatser")
def beaches_in_Sthml():
    """Visar lista på badplatser i Stockholm med tillhörande koordinater"""

    ## Inhämtar data om badplater från extern API
    data_url = f"https://apigw.stockholm.se/api/PublicHittaCMS/api/serviceunits?&filter[servicetype.id]=104&page[limit]=1500&page[offset]=0&sort=name"

    ## Anropar funktionen som konverterar json data till python och sparar i variabel.
    beach_list=func.json_loads_on_uncorrected_list(data_url)

    ## Lista på badplatser med tillhörande url för detaljerad info
    beach_info = []

    ## Iteration för att spara namn och url för varje badplats som dictionary i listan beach_info
    for info in beach_list["data"]:
        beach_name_unicode=info["attributes"]["name"]
        beach_link = info["links"]["self"]
        beach_info.append({"name": beach_name_unicode, "url": beach_link})

    ## Iteration för att komma åt varje enskild badplats url.
    url_list=[]
    for url in beach_info:
        data_url = url["url"]
        url_list.append(data_url)


    ## Lägga stadsdel för badplatser som ordbok i en lista.
    beach_name_info = []

    for one_url in url_list:
        """Här inhämtar jag mer info från en annan API"""
        beach_url = func.json_loads_on_uncorrected_list(one_url)
        for detailed_info in beach_url["included"]:
            if "name" in detailed_info["attributes"]:
                beach_location = detailed_info["attributes"]["name"]
                beach_name_info.append({"location": beach_location})
                break

    ## Här skapar jag en lista med ordböcker som jag får vid sammanslagningen av 2 olika listor.
    complete_beach_list=[]

    ## Använder funktionen zip för sammanslagningen av listorna med mer info om varje badplats.
    for a, b in zip(beach_info, beach_name_info):
        complete_dict=dict(list(a.items()) + list(b.items()))
        complete_beach_list.append(complete_dict)

    # Funktion för att söka stränder på samma location:
    #search_place = "Bromma"
    #for place in complete_beach_list:
        #if place["location"]== search_place:
            #return place["name"]

    # Funktion för att söka badplats och visa location
    #search_beach = "Tanto strandbad"
    #for place in complete_beach_list:
        #if place["name"]== search_beach:
            #return place["location"]

    ## Ny lista, nu väljer jag kolumnnamn till tabellen istället för nycklar.
    list_column_name = [{"Badplats": element["name"], "Stadsdel": element["location"]} for element in complete_beach_list]

    ## Konverterar listan till en tabell med pandas, utan index.
    df = pd.DataFrame(list_column_name)
    table_data=df.to_html(index=False)

    return table_data

    # Med denna return visas html template med rullista så att man kan välja bad/ställe:
    ## render_template("badplats.html", complete_beach_list=complete_beach_list)


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
        try:
            read_link = random_book['formats']['text/html']
        except:
            read_link = "https://gutenberg.org/"
        try:
            cover = random_book['formats']['image/jpeg']
        except:
            cover = "Ingen omslagsbild laddades"

        
    else:
        title = "Boken misslyckades med att laddas!"

    return render_template('books.html', title=title, author=author, downloads_number=downloads_number, read_link=read_link, cover=cover)
  


@app.route("/books_form", methods =["GET", "POST"])

def books_form():

    if request.method == 'POST':
    
        topic = request.form.get('topic')

        api_url = f"https://gutendex.com/books/?topic={topic}"
        
        response = requests.get(api_url)

        # if the api is responsive
        if response.status_code == 200:

            #getting the full response from a webpage
            books = response.json()

            data = func.build_df(books)

        else:
            data = "Boker misslyckades med att laddas!"
        
        return render_template('books_form.html', data=data)

    else:

        return render_template('books_form.html')
    
@app.route('/', methods=['GET', 'POST'])

def movie_viewer():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        # api key for omdb
        api_key = "1d6bf689"
        url = f"https://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            movie_info = response.json()

            if movie_info:
                return render_template('index.html', movie_info=movie_info)
            
        return "Movie information not found."
    
    return render_template('film.html')

@app.route("/anything")
def random_anything():
    response = requests.get("https://www.boredapi.com/api/activity")

    if response.status_code == 200:
        data = response.json()
        anything_suggestion = data.get("activity")
    else:
        anything_suggestion = "Kunde inte hämta aktivitetsförslag från API."

    return render_template("anything.html", anything_suggestion=anything_suggestion)



@app.errorhandler(404)
def not_found_error(error):
    return render_template("/errorhandler.html")
  

if __name__ == "__main__":
    app.run(debug=True)

