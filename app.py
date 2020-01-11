import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)


# -------------------- #
#    DB Collections    #
# -------------------- #
MONGODB_URI = os.environ.get("MONGO_PM_MONGO")
DBS_NAME = "recipes_db"
COLLECTION_NAME = "desserts"
app.config["MONGO_URI"] = os.getenv("MONGO_PM_MONGO")

mongo = PyMongo(app)

# -------------------- #
#        Routes        #
# -------------------- #
@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.desserts.find())

@app.route('/add_recipe')
def add_recipe():
    _uom = mongo.db.units_of_measurement.find()
    uom_list = [uom for uom in _uom]
    return render_template("addrecipe.html", recipes=mongo.db.desserts.find())

"""INSERT RECIPE TO MONGODB FUNCTION"""
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    desserts = mongo.db.desserts
    desserts.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), 
        port=int(os.environ.get('PORT', 5000)),
        debug=True)