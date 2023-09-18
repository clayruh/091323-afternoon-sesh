#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Hero, Villain, HeroVillain

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

@app.get('/debug')
def debug():
    import ipdb; ipdb.set_trace()
    return "Debugging! Yay!"


# CREATE
@app.post('/villains')
def create_villain():
    # imported from Flask. request object(headers, status code, but more specifically, we're asking for the JSON)
    villain_data = request.json
    # print(villain_data)

    # rebuild Villain w the data
    villain = Villain(name=villain_data["name"], secret_lair=villain_data["secret_lair"], childhood_trauma=villain_data["childhood_trauma"])

    db.session.add(villain)
    db.session.commit()

    return villain.to_dict(), 201

# READ
@app.get('/heroes')
def all_heroes():
    heroes = Hero.query.all()
    # here we've defined to_dict() function
    return [hero.to_dict() for hero in heroes], 200

@app.get('/heroes/<int:id>')
def hero_by_id(id: int):
    try: 
        hero = Hero.query.filter(Hero.id == id).first()
        response = hero.to_dict()
        return response, 200
    except Exception as e:
        return {'error': "404 not found"}, 404

@app.get('/villains')
def all_villains():
    villains = Villain.query.all()
    # print(villains)
    return [villain.to_dict(rules=("-herovillains",)) for villain in villains], 200

@app.get('/villains/<int:id>')
def villain_by_id(id):
    try: 
        villain = Villain.query.filter(Villain.id == id).first()
        response = villain.to_dict()
    except AttributeError:
        return {"error": "404 not found"}

    return response, 200

# UPDATE
@app.patch('/villains/<int:id>')
def update_villain(id): 
    data_to_update = request.json
    Villain.query.filter(Villain.id == id).update(data_to_update)
    db.session.commit()

    villain = Villain.query.filter(Villain.id == id).first()

    return villain.to_dict(), 202

# DELETE
@app.delete('/villains/<int:id>')
def delete_villain(id):
    try:
        villain = Villain.query.filter(Villain.id == id).first()
        db.session.delete(villain)
        db.session.commit()
        return {}, 204
    except:
        return {"error": "404 Could not delete, not found"}, 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
