import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
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
@app.route('/homepage_index')
def homepage_index():
    ###if 'username' in session:
       ### return 'You are logged in as ' + session['username']
    return render_template("index.html", recipes=mongo.db.desserts.find()) 
    
    carousel = (
       [recipe for recipe in recipes_collection.aggregate([
           {"$sample": {"size": 8}}])])
    return render_template("index.html", carousel=carousel)

@app.route('/user/login', methods = ["POST", "GET"])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']}) 
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if 'user' in session:
            return redirect (url_for('user'))

    return render_template('login.html')

@app.route('/user')
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{{user}}</h1>"

@app.route('/user/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))  

@app.route('/user/signup', methods=["POST"])
def signup():
    return render_template('signup.html')

@app.route('/recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.desserts.find())

@app.route('/recipes/new')
def add_recipe():
    _uom = mongo.db.units_of_measurement.find()    
    return render_template("addrecipe.html", uom=_uom)

@app.route('/recipe/<dessert_id>')
def view_recipe(dessert_id):
    the_recipe = mongo.db.desserts.find_one({"_id": ObjectId(dessert_id)})
    return render_template("viewrecipe.html", recipe=the_recipe)

@app.route('/recipe/<dessert_id>/edit')
def edit_recipe(dessert_id):
    the_recipe = mongo.db.desserts.find_one({"_id": ObjectId(dessert_id)})    
    return render_template('editrecipe.html', recipe=the_recipe)

@app.route('/recipe/<dessert_id>/update', methods=["POST"])
def update_recipe(dessert_id):
    desserts = mongo.db.desserts
    recipe_edit = {
        'recipe_name':request.form.get('recipe_name'),
        'recipe_description':request.form.get('recipe_description'),
        'ingredients':request.form.get('ingredients'),
        'equipment_needed':request.form.get('equipment_needed'),
        # 'method':request.form.get['method'],
        'gluten_free':request.form.get('gluten_free'),
        'contains_nuts':request.form.get('contains_nuts'),
        'vegan_friendly':request.form.get('vegan_friendly')
    }
    desserts.update_one({"_id": ObjectId(dessert_id)}, recipe_edit),  
    return redirect(url_for('get_recipes'))

@app.route('/recipe/insert', methods=['POST'])
def insert_recipe():
    desserts = mongo.db.desserts    
    recipe_to_be_inserted = request.form
    recipe = recipe_to_be_inserted.to_dict()
    desserts.insert_one(recipe)
    return redirect(url_for('get_recipes'))

@app.route('/recipe/<dessert_id>/delete')
def delete_recipe(dessert_id):
    mongo.db.desserts.delete_one({'_id': ObjectId(dessert_id)})
    return redirect(url_for('get_recipes'))

###EQUIPMENT
@app.route('/equipment')
def get_equipment():
    return render_template('equipment.html', equipment=mongo.db.equipment.find())

# -------------------- #
#   Other Functions    #
# -------------------- #
###Dropdown
def dropdown_uom():
    return [
        item for measurement in unit_of_measurement.find()
        for item in measurement.get("uom_name")]


    # import pdb; pdb.set_trace()

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
