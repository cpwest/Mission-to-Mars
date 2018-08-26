# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.collection.find()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_info()
    
    mars.update({}, mars_data, upsert=True)

    mongo.db.collection.insert_one()
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)