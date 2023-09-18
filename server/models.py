from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# even though db.Model and SerializerMixin have the same functions, the second inheritance overwrites
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    power = db.Column(db.String)
    weakness = db.Column(db.String)

    herovillains = db.relationship("HeroVillain", back_populates='hero')
    # want to be able to write hero1.villains and show all the associations
    # villains = association_proxy('the middle bridge relationship', 'relationship variable/endpoint')
    villains = association_proxy('herovillains', 'villain')

    # prevent recursion, so use serialize_rules ('- do not give me this!'). takes iterable, so list or tuple. don't bounce back '-herovillains.SELF'
    '''serialize_rules = ('-herovillains.hero',)'''
    # restructure the code to be more like heroes: {"villains": []}
    serialize_rules = ('-herovillains', 'villains', '-villains.heroes', '-villains.herovillains')

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "power": self.power,
    #         "weakness": self.weakness,
    #         # make a dictionary of each villain attached to hero
    #         "villains": [villain.to_dict() for villain in self.villains]
    #     }

class Villain(db.Model, SerializerMixin):
    __tablename__ = 'villains'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    secret_lair = db.Column(db.String)
    childhood_trauma = db.Column(db.String)

    herovillains = db.relationship("HeroVillain", back_populates="villain")
    heroes = association_proxy('herovillains', 'hero')

    serialize_rules = ('-herovilllains.villain', '-herovillains.hero.villains', '-herovillains.villain_id')

    # def to_dict_with_heroes(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "heroes": [hero.to_dict() for hero in self.heroes]
    #     }
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #     }

class HeroVillain(db.Model, SerializerMixin):
    __tablename__ = 'heroesvillains'
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    villain_id = db.Column(db.Integer, db.ForeignKey('villains.id'))

    hero = db.relationship("Hero", back_populates='herovillains')
    villain = db.relationship("Villain", back_populates='herovillains')

    # because this table is connected to two tables. "when you go to hero, don't come back to herovillains + when you go to villain, don't come back to herovillains"
    serialize_rules = ('-hero.herovillains','-villain.herovillains')