#!/usr/bin/env python3
import string

from flask import abort, flash Flask
from flask import render_template, request, redirect, jsonify, url_for
from flask import session as login_session

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

from apiclient import discovery
import httplib2
from oauth2client import client
import json
from flask import make_response
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///categories.db"
db = SQLAlchemy(app)

CLIENT_ID = json.loads(open("client_secrets.json", "r").read())[
    "web"]["client_id"]

# Preload all the categories here since they won't change.
categories = db.session.query(Category).order_by(asc(Category.id)).all()

# Login with Google Login
@app.route("/gconnect", methods=["POST"])
def gconnect():
    # If this request does not have `X-Requested-With` header, this could be a
    # CSRF
    if not request.headers.get("X-Requested-With"):
        response = make_response(json.dumps("Not authorized!"), 403)
        response.headers["Content-Type"] = "application/json"
        return response

    # Set path to the Web application client_secret_*.json file you downloaded
    # from the Google API Console:
    # https://console.developers.google.com/apis/credentials
    CLIENT_SECRET_FILE = "client_secrets.json"

    auth_code = request.data
    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ["https://www.googleapis.com/auth/drive.appdata", "profile", "email"],
        auth_code,
    )

    # Call Google API http_auth = credentials.authorize(httplib2.Http())
    # drive_service = discovery.build('drive', 'v3', http=http_auth)
    # appfolder = drive_service.files().get(fileId='appfolder').execute()
    guser_id = credentials.id_token["sub"]
    stored_access_token = login_session.get("access_token")
    stored_guser_id = login_session.get("user_id")
    if stored_access_token is not None and guser_id == stored_guser_id:
        response = make_response(
            json.dumps("Current user is already connected."), 200)
        response.headers["Content-Type"] = "application/json"
        return response

    print(str(credentials.id_token))
    # Store the access token in the session for later use.
    login_session["access_token"] = credentials.access_token
    login_session["user_id"] = guser_id
    login_session["username"] = credentials.id_token["name"]
    login_session["picture"] = credentials.id_token["picture"]
    login_session["email"] = credentials.id_token["email"]

    try:
        db.session.query(User).filter_by(id=guser_id).one()
    except BaseException:
        newUser = User(
            id=login_session["user_id"],
            name=login_session["username"],
            email=login_session["email"],
            group="google",
        )
        print("Adding user " + guser_id + " in database")
        db.session.add(newUser)
        db.session.commit()

    return "You have logged in!"


# DISCONNECT - Revoke a current user's token and reset their login_session.
@app.route("/gdisconnect")
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get("access_token")
    if access_token is None:
        response = make_response(
            json.dumps("Current user not connected."), 401)
        response.headers["Content-Type"] = "application/json"
        return response
    url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
    h = httplib2.Http()
    result = h.request(url, "GET")[0]
    del login_session["access_token"]
    del login_session["user_id"]
    del login_session["username"]
    del login_session["email"]
    del login_session["picture"]
    if result["status"] == "200":
        response = make_response(json.dumps("Successfully disconnected."), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        response = make_response(
            json.dumps("Failed to revoke token for given user.", 400)
        )
        response.headers["Content-Type"] = "application/json"
        return response


# Index page.
@app.route("/")
def showIndexPage():
    last_10_items = (
        db.session.query(Item).order_by(desc(Item.create_time)).limit(10).all()
    )
    return render_template(
        "index.html", categories=categories, items=last_10_items)


# Category page.
@app.route("/category/<string:category_name>/items")
def showCategory(category_name):
    category = db.session.query(Category).filter_by(name=category_name).one()
    items = db.session.query(Item).filter_by(category_id=category.id).all()
    return render_template(
        "category.html",
        items=items,
        item_count=len(items),
        category=category,
        categories=categories,
    )


# Item page.
@app.route("/category/<string:category_name>/<string:item_name>")
def showItem(category_name, item_name):
    try:
        category = db.session.query(Category).filter_by(
            name=category_name).one()
        item = (
            db.session.query(Item)
            .filter_by(name=item_name, category_id=category.id)
            .one()
        )
        has_access = False
        if "user_id" in login_session and (
          login_session["user_id"] == item.user_id):
            has_access = True
        return render_template("item.html", item=item, has_access=has_access)
    except BaseException:
        return abort(404)


def queryItemAndCheckAccess(item_name):
    if "username" not in login_session:
        abort(403)

    try:
        item = db.session.query(Item).filter_by(name=item_name).one()
        if login_session["user_id"] != item.user_id:
            abort(403)
    except BaseException:
        abort(404)

    return item


# Add Item page.
@app.route("/category/addItem/", methods=["GET", "POST"])
def addItem():
    if "username" not in login_session:
        abort(403)

    if request.method == "POST":
        newItem = Item(
            name=request.form["name"],
            description=request.form["description"],
            category_id=request.form["category_id"],
            user_id=login_session["user_id"],
        )
        db.session.add(newItem)
        db.session.commit()
        flash("Item %s Added Successfully" % (newItem.name))
        return redirect(url_for("showIndexPage"))
    else:
        return render_template("addItem.html", categories=categories)


# Edit item page.
@app.route("/category/<string:item_name>/editItem/", methods=["GET", "POST"])
def editItem(item_name):
    item = queryItemAndCheckAccess(item_name)
    if request.method == "POST":
        item.name = request.form["name"]
        item.description = request.form["description"]
        item.category_id = request.form["category_id"]

        db.session.add(item)
        db.session.commit()
        flash("Item %s Edited Successfully" % (item.name))
        return redirect(url_for("showIndexPage"))
    else:
        return render_template(
            "editItem.html", categories=categories, item=item)


# Delete Item page.
@app.route("/category/<string:item_name>/deleteItem/", methods=["GET", "POST"])
def deleteItem(item_name):
    item = queryItemAndCheckAccess(item_name)
    if request.method == "POST":
        item = db.session.query(Item).filter_by(name=item_name).one()
        flash("Item %s Deleted Successfully" % (item.name))
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for("showIndexPage"))
    else:
        return render_template("deleteItem.html", categories=categories)


# API to get the most recent n created item.
@app.route("/api/latest_items")
def latestItemApi():
    try:
        num = request.args.get("n")
    except BaseException:
        num = 10

    latest_items = (
        db.session.query(Item).order_by(
            desc(Item.create_time)).limit(num).all()
    )
    return jsonify(items=[i.serialize for i in latest_items])


# API to get all categories data.
@app.route("/api/category/all")
def allCategoryApi():
    return jsonify(categories=[i.serialize for i in categories])


# API to get all items in a specific category.
@app.route("/api/category/<string:category_name>")
def categoryItemsApi(category_name):
    try:
        num = request.args.get("n")
    except BaseException:
        num = 10

    try:
        category = db.session.query(Category).filter_by(
            name=category_name).one()
        items = (
            db.session.query(Item).filter_by(
                category_id=category.id).limit(num).all()
        )
        return jsonify(categories=[i.serialize for i in items])
    except BaseException:
        return jsonify(
            {"error": "%s is not a valid category." % category_name})


# API to a specific item in a category.
@app.route("/api/category/<string:category_name>/<string:item_name>")
def itemApi(category_name, item_name):
    try:
        category = db.session.query(Category).filter_by(
            name=category_name).one()
    except BaseException:
        return jsonify(
            {"error": "%s is not a valid category." % category_name})

    try:
        item = (
            db.session.query(Item)
            .filter_by(name=item_name, category_id=category.id)
            .one()
        )
        return jsonify(categories=item.serialize)
    except BaseException:
        return jsonify(
            {"error": "%s doesn't exist in category %s." %
                (item_name, category_name)}
        )


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
