import os
import math
from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from flask_pymongo import PyMongo, pymongo
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter, get_page_args
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
app.secret_key = os.getenv("SECRET_KEY")

mongo = PyMongo(app)

# -------------------- #
#        Routes        #
# -------------------- #
###RECIPES
@app.route('/')
def homepage_index():
    return render_template("index.html", recipes=mongo.db.desserts.aggregate(
        [{'$sample': {'size': 3 }}]
        ))

###@app.route('/user/login/page')
###def login_page():
    ###users = mongo.db.users
    ###return render_template('login.html')

###@app.route('/user/login', methods = ["POST", "GET"])
###def login():
    ###users = mongo.db.users
    ###login_user = users.find_one({'name': request.form['username']}) 
    ###if request.method == "POST":
        ###user = request.form["nm"]
        ###session["user"] = user
        ###return redirect(url_for("user"))
    ###else:
        ###if 'user' in session:
            ###return redirect (url_for('user'))

    ###return render_template('login.html')

###@app.route('/user')
###def user():
    ###if "user" in session:
        ###user = session["user"]
        ###return f"<h1>{{user}}</h1>"

###@app.route('/user/logout')
###def logout():
    ###session.pop("user", None)
    ###return redirect(url_for('login'))  

###@app.route('/user/signup', methods=["POST"])
###def signup():
    ###return render_template('signup.html')

def paginate_recipes(offset=0, per_page=6):
    recipes = mongo.db.desserts
    offset = get_page_items
    return recipes[offset: offset + per_page]

#Recipes Page
@app.route('/recipes/',defaults={'page': 1}, methods=['GET']) #defaults={'page': 1},
@app.route('/recipes/page/<int:page>', methods=['GET'])
    
def get_recipes(page):

    dessert = mongo.db.desserts
    #First Page
    #desserts = dessert.find({'_id': {'$gte': last_id}}).sort('recipe_name', pymongo.ASCENDING).limit(6)
    #Second Page
    #dessert.find({'_id': {'$gte': last_id}}).sort('recipe_name', pymongo.ASCENDING).limit(6).skip(6)
    #Third Page
    #dessert.find({'_id': {'$gte': last_id}}).sort('recipe_name', pymongo.ASCENDING).limit(6).skip(6)
    total = mongo.db.desserts.count()
    limit = 6
    num_of_pages = total/limit + 1
    pagination = get_pagination(page=page,
                            per_page=limit,   #results per page
                            total=total,         #total number of results 
                            format_total=True,   #format total. example 1,024
                            format_number=True,  #turn on format flag
                            record_name='recipes', #provide context
                            )
    #page_number = int
    #skipped = (page_number - 1) * limit
    offset = 0
    starting_id = dessert.find().sort('_id', pymongo.ASCENDING)
    last_id = starting_id[offset]['_id']
    desserts = dessert.find({'_id': {'$gte': last_id}}).sort('recipe_name', pymongo.ASCENDING).limit(limit)
    documents_cursor = mongo.db.desserts.find() # returns a cursor. you can sort at this point
    desserts_in_page = documents_cursor.skip(6).limit(limit)
    
    return render_template("recipes.html", recipes=desserts, pagination=pagination, page=page,
    total=total, per_page=limit)


@app.route('/recipes/new')
def add_recipe():
    _uom = mongo.db.units_of_measurement.find()    
    return render_template("addrecipe.html", uom=_uom)

#Adding Recipe
@app.route('/recipe/insert', methods=['POST'])
def insert_recipe():
    desserts = mongo.db.desserts    
    recipe_to_be_inserted = request.form
    recipe = recipe_to_be_inserted.to_dict()
    desserts.insert_one(recipe)
    return redirect(url_for('insert_success'))

#Recipe Added - Success Screen
@app.route('/recipe/success')
def insert_success():
    return render_template("recipeadded.html")


#View Individual Recipe
@app.route('/recipe/<dessert_id>')
def view_recipe(dessert_id):
    the_recipe = mongo.db.desserts.find_one({"_id": ObjectId(dessert_id)})
    return render_template("viewrecipe.html", recipe=the_recipe)

#Edit Selected Recipe
@app.route('/recipe/<dessert_id>/edit')
def edit_recipe(dessert_id):
    the_recipe = mongo.db.desserts.find_one({"_id": ObjectId(dessert_id)})    
    return render_template("editrecipe.html", recipe=the_recipe)


#Updating Recipe In MongoDB
@app.route('/recipe/<dessert_id>/update', methods=["GET", "POST"])
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
    desserts.update({"_id": ObjectId(dessert_id)}, recipe_edit),  
    return redirect(url_for('edit_success'))

#Recipe Updated - Success Screen
@app.route('/recipe/editsuccess')
def edit_success():    
    return render_template('recipeupdated.html')

#Deleting Recipe
@app.route('/recipe/<dessert_id>/delete')
def delete_recipe(dessert_id):
    mongo.db.desserts.delete_one({'_id': ObjectId(dessert_id)})
    return redirect(url_for('delete_success'))

#Recipe Deleted - Success Screen
@app.route('/recipe/deleted')
def delete_success():
    return render_template("recipedeleted.html")


###EQUIPMENT
@app.route('/equipment')
def get_equipment():

    shop = mongo.db.equipment

    offset = int(request.args.get('offset')) if request.args.get('offset') else 1
    limit = int(request.args.get('limit')) if request.args.get('offset') else 8
    page = int(request.args.get('page', 2))
    total = mongo.db.equipment.count()
    per_page = limit
    pagination = get_pagination(page=page,
                            per_page=per_page,   #results per page
                            total=total,         #total number of results 
                            format_total=True,   #format total. example 1,024
                            format_number=True,  #turn on format flag
                            record_name='repositories', #provide context
                            )
    starting_id = shop.find().sort('_id', pymongo.ASCENDING)
    last_id = starting_id[offset]['_id']

    equipment = shop.find({'_id': {'$gte': last_id}}).sort('item_name', pymongo.ASCENDING).limit(limit)
    
    next_url='/equipment?limit=' + str(limit) + '&offset=' + str(offset + limit)
    prev_url='/equipment?limit=' + str(limit) + '&offset=' + str(offset - limit)

    pagination = Pagination(page=page,limit=limit)
    #return jsonify ({'result': output, 'prev_url': '', 'next_url': ''})
    
    return render_template('equipment.html', equipment=equipment, pagination=pagination)

# -------------------- #
#   Other Functions    #
# -------------------- #
###Pagination - copied from https://harishvc.com/2015/04/15/pagination-flask-mongodb/
def get_css_framework():
    return 'bootstrap4'
def get_link_size():
    return 'sm'  #option lg
def show_single_page_or_not():
    return False
def get_page_items():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page')
    if not per_page:
        per_page = PER_PAGE
    else:
        per_page = int(per_page)
    offset = (page - 1) * per_page
    return page, per_page, offset
def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'repositories')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )

###Dropdown
def dropdown_uom():

    uom = mongo.db.unit_of_measurement

    return [
        item for measurement in uom.find()
        for item in measurement.get("uom_name")]


    # import pdb; pdb.set_trace()

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
