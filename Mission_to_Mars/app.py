import pymongo
import scrape_mars
from flask import Flask, jsonify, redirect, render_template
from flask_pymongo import PyMongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():

	# Find one record of data from thr mongo database
	mars = mongo.db.collection.find_one()


	# Return template and date
	return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():

	#run the scrape function
	mars_data = scrape_mars.scrape()

	# update the Mongo database using update and upsert=True
	mongo.db.collection.update({}, mars_data, upsert=True)

	# Redirect back to home page
	return redirect("/")


if __name__ == '__main__':
	app.run(debug=True)
