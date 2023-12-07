from flask import Flask, render_template, request

app = Flask(__name__)

def get_pokemon_data(pokemon):
   url = f'https://pokeapi.co/api/v2/ {pokemon}'
   r= request.get(url).json()
   return r


@app.route("/")
def home():
    return render_template('pokemon.html')

@app.route("/detalle")
def detalle():
    return render_template('detalle.html')




if __name__ == '__main__':
    app.run(debug=True)