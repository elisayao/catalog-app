#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base

engine = create_engine('sqlite:///categories.db')
Base.metadata.create_all(engine)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

print("Initialize categories.")
category_names = [
    'Soccer',
    'Basketball',
    'BaseBall',
    'Frisbee',
    'Snowboarding',
    'Rock Climbing',
    'Foosball',
    'Skating',
    'Hockey']

for name in category_names:
    print("Create new category:" + name)
    new_category = Category(name=name)
    session.add(new_category)

session.commit()
