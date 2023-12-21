from flask import Flask,render_template,request
import requests
from dotenv import load_dotenv, dotenv_values


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///pokedex.sqlite"

db=SQLAlchemy(app)

class Pokemon(db.Model):
    id: Mapped[int] = mapped_column(db.Integer,primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(db.String,nullable=False)
    height: Mapped[float] = mapped_column(db.Float,nullable=False)
    weight: Mapped[float] = mapped_column(db.Float,nullable=False)
    order: Mapped[int] = mapped_column(db.Integer,nullable=False)
    type: Mapped[str] = mapped_column(db.String,nullable=False)

with app.app_context():
    db.create_all()
    
def get_pokemon_data(pokemon):
    url=f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    r = requests.get(url).json()
    return r

@app.route("/", methods=['GET','POST'])
def home():
    pokemon = None
    if request.method == 'POST':
        name_pokemon = request.form.get('name')
        if name_pokemon: 
            data = get_pokemon_data(name_pokemon.lower())#el nombre del pokemon se lee en minuscula.
            if data:
                pokemon={'id':data.get('id'), 
                        'name':data.get('name').upper(),#con esta sentencia buscamos el json
                        'height': data.get('height'), 
                        'weight':data.get('weight'),
                        'order':data.get('order'),
                        'type':'Profesor',
                        'photo':data.get('sprites').get('other').get('official-artwork').get('front_default'),
                        }
    return render_template('pokemon.html', pokemon=pokemon)


#@app.route("/detalle/<hp>/<attack>/<defence>/<speed>/")
#def detalle(hp,attack,defence,speed):
#    return render_template('detalle.html', hp=hp, attack=attack, defence=defence, speed=speed)

@app.route("/detalle/<id>")
def detalle(id):
    data = get_pokemon_data(id)
    pokemon = {
        'photo': data.get("sprites").get("other").get("dream_world").get("front_default"),
        'name': data.get("name").upper(),
        'hp': data.get("stats")[0].get("base_stat"),
        'attack': data.get("stats")[1].get("base_stat"),
        'defence': data.get("stats")[2].get("base_stat"),
        'speed': data.get("stats")[5].get("base_stat"),
    }
    return render_template("detalle.html", pokemon=pokemon)
 
#Agregar la información a la base de datos
#@app.route("/insert_pokemon/<pokemon>")
#def insert(pokemon):
#       new_pokemon=pokemon
#    if new_pokemon:
#        obj=pokemon  #obj=Pokemon(pokemon) 
#        db.session.add(obj)
#        db.session.commit()
#   return 'Pokemon Agregado'


#@app.route("/select/<name>")
#def selectbyname(name):
#    poke = Pokemon.query.filter_by(name=name).first()
#    return str(poke.id) + str(poke.name)

#@app.route("/selectbyid/<id>")
#def selectbyid(id):
#    poke = Pokemon.query.filter_by(id=id).first()
#    return str(poke.id) + str(poke.name)

#@app.route("/deletebyid/<id>")
#def deletebyid(id):
#    pokemon_a_eliminar = Pokemon.query.filter_by(id=id).first()
#    db.session.delete(pokemon_a_eliminar)
#    db.session.commit()
#    return 'Pokemon Eliminado!'


if __name__=='__main__':
    app.run(debug=True)
    
    
