#!/usr/bin/env python3

import random
from app import app
from models import db, Hero, Villain, HeroVillain
from faker import Faker

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        print("Removing old data...")
        Hero.query.delete()
        Villain.query.delete()
        HeroVillain.query.delete()

        print("Seeding heroes...")

        heroes = []
        powers = ("lazers", "remembering syntax", "invisibility", "teleportation", "telekinesis")

        for _ in range (25):
            hero = Hero(name=faker.name(), power=random.choice(powers), weakness="childhood trauma probably")
            heroes.append(hero)
        db.session.add_all(heroes)
        db.session.commit()

        print("Seeding villains...")
        villains = []
        childhood_traumas = ["single parent", "scientology", "climate disaster", "affluenza"]

        for _ in range(50):
            villain = Villain(name=faker.name(), secret_lair=faker.address(), childhood_trauma=random.choice(childhood_traumas))
            villains.append(villain)
        db.session.add_all(villains)
        db.session.commit()

        print("Seeding herovillain relationships...")
        herovillains = []

        for _ in range(100):
            hv = HeroVillain(hero=random.choice(heroes), villain=random.choice(villains))
            herovillains.append(hv)
        db.session.add_all(herovillains)
        db.session.commit()

        print("Seeding complete!")
