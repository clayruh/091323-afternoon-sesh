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
    return [villain.to_dict() for villain in villains], 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
