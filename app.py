import os
import math
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo, pymongo
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter, get_page_args
import bcrypt
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env
from werkzeug.security import generate_password_hash, check_password_hash


###App Config     

app = Flask(__name__)

app.secret_key = b'ab245pfd20\n\xec]/'

###DB Collections
MONGODB_URI = os.environ.get("MONGO_PM_MONGO")
DBS_NAME = "recipes_db"
COLLECTION_NAME = "desserts"
app.config["MONGO_URI"] = os.getenv("MONGO_PM_MONGO")
#app.secret_key = os.getenv("SECRET_KEY")
mongo = PyMongo(app)
users = mongo.db.users


###Routes
#Homepage
@app.route('/')
def homepage_index():
    return render_template("landing.html", recipes=mongo.db.desserts.aggregate(
        [{'$sample': {'size': 3 }}]
        ))

@app.route('/user/homepage')
def user_home():
    return render_template("index.html", recipes=mongo.db.desserts.aggregate(
        [{'$sample': {'size': 3 }}]
        ))


###User Authentication 
#Login/Register
@app.route('/user/signup', methods=["GET", "POST"])
def signup():
    # Check if user is not logged in already
	#if 'user' in session:
	#	flash('You are already sign in!')
	#	return redirect(url_for('user_home'))
	if request.method == 'POST':
		form = request.form.to_dict()
		# Check if the password and password1 match 
		if form['password'] == form['password1']:
			# If so try to find the user in db
			user = users.find_one({"username" : form['username']})
			if user:
				flash(f"{form['username']} already exists!")
				return redirect(url_for('signup'))
			# If user does not exist register new user
			else:				
				# Hash password
				hash_pass = generate_password_hash(form['password'])
				#Create new user with hashed password                
				users.insert_one(
					{
						'username': form['username'],
						'email': form['email'],
						'password': hash_pass
					}
				)
				# Check if user is saved
				user_in_db = users.find_one({"username": form['username']})
				if user_in_db:
					# Log user in (add to session)
					session['user'] = user_in_db['username']
					return redirect(url_for('profile', user=user_in_db['username']))
				else:
					flash("There was a problem saving your profile")
					return redirect(url_for('signup'))

		else:
			flash("Passwords dont match!")
			return redirect(url_for('signup'))
		
	return render_template("signup.html")

# Log out
@app.route('/logout')
def logout():
	# Clear the session
	session.clear()
	flash('You were logged out!')
	return redirect(url_for('homepage_index'))

# Profile Page
@app.route("/profile/<user>", methods=["GET", "POST"])
def profile(user): 
	# Check if user is logged in
	if 'user' in session:
		# If so get the user and pass him to template for now
		user_in_db = users.find_one({"username": user})
		return render_template('profile.html', user=user_in_db)
	else:
		flash("You must be logged in!")
		return redirect(url_for('user_home'))


@app.route('/user/login/page')
def login_page():
    users = mongo.db.users
    return render_template('login.html')

@app.route('/user/login', methods = ["GET"])
def login():
	# Check if user is not logged in already
	if 'user' in session:
        
		user_in_db = users.find_one({"username": session['user']})
        
		if user_in_db:
			# If so redirect user to their profile
			#flash("You are logged in already!")
            #session['user'] = user_in_db['username']
			return redirect(url_for('profile', user=user_in_db['username']))
	else:
		# Render the page for user to be able to log in
            return render_template('login.html')


# Check user login details from login form
@app.route('/user_auth', methods=['POST'])
def user_auth():
	form = request.form.to_dict()
	user_in_db = users.find_one({"username": form['username']})
	# Check for user in database
	if user_in_db:
		# If passwords match (hashed / real password)
		if check_password_hash(user_in_db['password'], form['user_password']):
            #session['user'] = user_in_db['username']
			flash("You were logged in!")
			return redirect(url_for('profile', user=user_in_db['username']))
			
		else:
			flash("Wrong password or user name!")
			return redirect(url_for('login'))
	else:
		flash("You must be registered!")
		return redirect(url_for('signup'))


#Pagination
def paginate_recipes(offset=0, per_page=6):
    recipes = mongo.db.desserts
    offset = get_page_items
    return recipes[offset: offset + per_page]


#Recipes Page
@app.route('/recipes/', methods=['GET']) 
    
def get_recipes():

    dessert = mongo.db.desserts
    
    total = mongo.db.desserts.count()
    
    offset = 0
    starting_id = dessert.find().sort('_id', pymongo.ASCENDING)
    last_id = starting_id[offset]['_id']
    desserts = dessert.find({'_id': {'$gte': last_id}}).sort('recipe_name', pymongo.ASCENDING)#.limit(limit)
    documents_cursor = mongo.db.desserts.find() 
    
    return render_template("recipes.html", recipes=desserts, total=total)


@app.route('/recipes/new')
def add_recipe():
    form = request.form.to_dict()
    user_in_db = users.find_one({"username": form['username']})
        # Check for user in database
    if user_in_db:
        session['userid'] = user_in_db._id
        return render_template("addrecipe.html", session=session) 
    else:    
	    return redirect(url_for('login'))


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
        'method':request.form.get['method'],
        'gluten_free':request.form.get('gluten_free'),
        'contains_nuts':request.form.get('contains_nuts'),
        'vegan_friendly':request.form.get('vegan_friendly'),
        'author':request.form.get('author'),
        'img_url':request.form.get('img_url')
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


### Other Functions    
#Pagination - copied from https://harishvc.com/2015/04/15/pagination-flask-mongodb/
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
        per_page = per_page
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

# app name 
@app.errorhandler(404) 
  
# inbuilt function which takes error as parameter 
def not_found(e): 
  
# defining function 
  return render_template("404.html") 


###Dropdown
def dropdown_uom():

    uom = mongo.db.unit_of_measurement

    return [
        item for measurement in uom.find()
        for item in measurement.get("uom_name")]


    # import pdb; pdb.set_trace()

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
    
