from flask import Flask, render_template, request
from dotenv import load_dotenv,dotenv_values 


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column



config = dotenv_values('.env')
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokedex.sqlite"

# Vinculamos la base de datos con la app
db = SQLAlchemy(app)

class Pokemon(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False)

# con esta sentencia se crea las tablas 
with app.app_context():
    db.create_all()



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


@app.route("/prueba")
def prueba():
    new_pokemon = 'Vaporeon'
    obj = Pokemon(name = new_pokemon)
    db.session.add(obj)
    db.session.commit()
    return 'Pokemon agregado'

@app.route("/busqueda/<name>")
def busqueda(name):
    poke = Pokemon.query.filter_by(name=name).first()
    return str(poke.id)
    

    return pokemon.id




if __name__ == '__main__':
    app.run(debug=True)
