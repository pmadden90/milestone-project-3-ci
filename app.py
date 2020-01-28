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
###RECIPES
@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.desserts.find())

@app.route('/add_recipe')
def add_recipe():
    _uom = mongo.db.units_of_measurement.find()
    uom_list = [uom for uom in _uom]
    return render_template("addrecipe.html", recipes=mongo.db.desserts.find())

@app.route('/edit_recipe/<dessert_id>')
def edit_recipe(dessert_id):
    the_recipe = mongo.db.desserts.find_one({"_id": ObjectId(dessert_id)})
    all_desserts = mongo.db.desserts.find()
    return render_template('editrecipe.html', recipe=the_recipe, dessert=all_desserts)

@app.route('/update_recipe/<dessert_id>', methods=["POST"])
def update_recipe(dessert_id):
    desserts = mongo.db.desserts
    desserts.update( {'_id: ObjectId(dessert_id)'},
    {
        'recipe_name':request.form.get['recipe_name'],
        'recipe_description':request.form.get['recipe_description'],
        'ingredients':request.form.get['ingredients'],
        'equipment_needed':request.form.get['equipment_needed'],
        'method':request.form.get['method'],
        'gluten_free':request.form.get['gluten_free'],
        'contains_nuts':request.form.get['contains_nuts'],
        'vegan_friendly':request.form.get['vegan_friendly']
    })
    return redirect(url_for('get_recipes'))

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    desserts = mongo.db.desserts
    desserts.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))

@app.route('/delete_recipe/<dessert_id>')
def delete_recipe(dessert_id):
    mongo.db.desserts.remove({'_id': ObjectId(dessert_id)})
    return redirect(url_for('get_recipes'))

###EQUIPMENT
@app.route('/get_equipment')
def get_equipment():
    return render_template('equipment.html', equipment=mongo.db.equipment.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), 
        port=int(os.environ.get('PORT', 5000)),
        debug=True)

# -------------------- #
#   Other Functions    #
# -------------------- #
###Dropdown
def dropdown_uom():
    return [
        item for measurement in unit_of_measurement.find()
        for item in measurement.get("uom_name")]