from flask import Flask, make_response, render_template, request, make_response
import requests
import random
from . import func
from application import func

app= Flask(__name__)


@app.route("/")
def weather():
    # Hämtar data om användaren
    info = func.json_loads("http://ipinfo.io/json")

    # Hämtar koordinater från den datan om användaren
    lat = info["loc"].split(",")[0]
    lon = info["loc"].split(",")[1]

    # Ser regn och molntäcke på de koordinaterna
    weather = func.json_loads(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=rain,snowfall,cloudcover")

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
@app.route("/badplatser", methods=["POST", "GET"])
def beaches_in_Sthml():
    """Denna endpoint hämtar info om badplatser i Stockholm från flera API:er. Visar användaren ett slumpmässigt förslag. Ger möjligheten att söka info
    om varje badplats samt söka badplatser efter stadsdel. Returnerar allt i fint format."""

    ## Inhämtar data om badplater från extern API
    data_url = f"https://apigw.stockholm.se/api/PublicHittaCMS/api/serviceunits?&filter[servicetype.id]=104&page[limit]=1500&page[offset]=0&sort=name"

    ## Anropar funktionen som konverterar json data till python och sparar i variabel.
    beach_list=func.json_loads(data_url)

    ## Lista på badplatser med tillhörande url för att inhämta mer info om varje resp badplats.
    beach_info = []

    ## Iteration för att spara namn och url för varje badplats som dictionary i listan beach_info
    for info in beach_list["data"]:
        beach_name=info["attributes"]["name"]
        beach_link = info["links"]["self"]
        beach_info.append({"name": beach_name, "url": beach_link})

    ## Iteration för att komma åt varje enskild badplats url.
    url_list=[]
    for url in beach_info:
        data_url = url["url"]
        url_list.append(data_url)

    ## Lägga stadsdel för badplatser som ordbok i en lista.
    beach_name_info = []

    for one_url in url_list:
        """Här inhämtar jag mer info varje badplats från en annan API"""
        beach_url = func.json_loads(one_url)
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

    ## Anropar funktion från func.py för att ge slumpnässigt förslag på badplats samt tillhörande stadsdel.
    random_beach = func.random_beach(complete_beach_list)

    ## Lista där stadsdel bara förekommer 1 gång, kan visas i rulllistan i badplats.html.
    unique_locations= []
    for dictionary in complete_beach_list:
        location = dictionary.get("location")
        if location and location not in unique_locations:
            # Om location inte i listan ska den läggas till
            unique_locations.append(location)

    ## Här följer koden som visar resultat för vald sökning, antingen badplats som visar var den ligger eller stadsdel för att hitta badplatser
    ### Skapar tom lista för att spara sökresultat



    matching_places = []
    ### När användaren skickar iväg data för sökning körs denna kod:
    if request.method == "POST":
    ### Hantera data som har skickats in via POST-förfrågan
        search_beach = request.form["selected_search"]
        search_location = request.form["selected_beach"]

        cookie_value = search_beach

        ### Söka badplats efter satdsdel och vice versa
        for places in complete_beach_list:
            if places["location"] == search_beach or places["name"] == search_location:
                ### Skriva ut sökresultat snyggt, inte som dict eller lista. Mer formattering i html filen.
                matching_places.append({"Badplats": places["name"], "Stadsdel": places["location"]})

        cookie_resp = make_response(render_template("badplats.html", random_beach=random_beach, complete_beach_list=complete_beach_list,
                           unique_locations=unique_locations, matching_places=matching_places, search_beach=search_beach))
        cookie_resp.status_code = 200
        cookie_resp.set_cookie("search_cookie", cookie_value)
        return cookie_resp

    else:
        search_cookie = request.cookies.get("search_cookie")
        return render_template("badplats.html", random_beach=random_beach, complete_beach_list=complete_beach_list,
                           unique_locations=unique_locations, matching_places=matching_places, cookie_value=search_cookie)
                           



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
        
        books_form_cookie=request.cookies.get('books_form_cookie')
        resp = make_response(render_template('books_form.html', data=data, books_form_cookie=books_form_cookie))
        resp.set_cookie('books_form_cookie', topic)
        return resp 


    else:

        return render_template('books_form.html')
    
@app.route('/film', methods=['GET', 'POST'])

def movie_viewer():
    if request.method == 'POST':
        movie_names = []
        with open ('movie_list.txt', 'r') as file:
            for line in file:
                movie_names.append(line.strip())
        random_movie_name = random.choice(movie_names)

        # api key for omdb
        api_key = "1d6bf689"
        url = f"https://www.omdbapi.com/?t={random_movie_name}&apikey={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            movie_info = response.json()

            if movie_info:
                return render_template('film.html', movie_info=movie_info)
            
        return "Movie information not found."
    response = make_response(render_template('film.html'))
    response.set_cookie('myCookie', 'myValue')
    return response

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
    message = "Page not found"
    return render_template("/errorhandler.html", message=message)

@app.errorhandler(405)
def not_found_error(error):
    message = "Method not allowed"
    return render_template("/errorhandler.html", message=message)
  

if __name__ == "__main__":
    app.run(debug=True)

