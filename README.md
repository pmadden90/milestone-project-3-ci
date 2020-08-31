
# Just Desserts

Just Desserts is a web based application for sharing recipes for desserts.
Users can add their own recipes (and then edit or delete them) or read other users' recipes. 
 
## UX
 
Use this section to provide insight into your UX process, focusing on who this website is for, what it is that they want to achieve and how your project is the best way to help them achieve these things.

####As a user, I want to browse and search for dessert recipes.

####As a user, I would like to see potential allergens in the recipes.

####As a registered user, I would like to submit my own recipes for others to see

####As a registered user, I would like to be able to edit my recipes and delete if necessary

####As a user, I would like to be able to find equipment I might want to purchase related to the recipes


Please use the following link to access the Figma Wireframe for Just Desserts - https://www.figma.com/file/pcRVh2MevzPhD7HzAyDv5l/Recipe-Site?node-id=0%3A1

## Features


 
### Existing Features
- REGISTRATION - allows users create profiles, by having them fill out a registration form
- LOGIN - allows previously registered users to log back in
- ADD RECIPES - allows users logged in to add a recipe to the database, by having them fill out a recipe form
- EDIT RECIPES - allows users logged in to edit the recipes they have previously submitted
- DELETE RECIPES - allows users logged in to delete the recipes they have previously submitted
- VIEW RECIPES - allows any users to view existing recipes in the database
- SHOP - allows users to view and purchase related equipment to baking


In addition, you may also use this section to discuss plans for additional features to be implemented in the future:

### Features Left to Implement
- The navbar link to personal profile - not working but intention would be for user to be able to see all their recipes on that page and ability to log out
- Initially, I attempted to set up a virtualenv as per suggestion of mentor however after discussing with a tutor via webchat, I discovered that a virtualenv is more difficult to set up on Gitpod 
so this was abandoned. 
- A rating system - up to 5 stars.
- I spent some time trying to implement a pagination function but it caused me delays and issues so decided to press on without it

## Technologies Used

In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.
- [Bootstrap]  (https://getbootstrap.com/)
    - The project uses **Bootstrap** for styling and layout.
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    
- [MongoDB] https://www.mongodb.com/)
    - The project uses **MongoDB** for creating, reading, updating and deleting data from a database.
- [Heroku]  (https://Heroku.com/)
    - The project uses **Heroku** for deploying and hosting the app.
- [Python] (https://python.org)


## Testing

#####As a user, I want to browse and search for dessert recipes.
Tested on Chrome, Edge and Firefox - working
#####As a user, I would like to see potential allergens in the recipes.
Tested on Chrome, Edge and Firefox - working
#####As a registered user, I would like to submit my own recipes for others to see

#####As a registered user, I would like to be able to edit my recipes and delete if necessary

#####As a user, I would like to be able to find equipment I might want to purchase related to the recipes
Tested on Chrome, Edge and Firefox - working

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Registration form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

Project has been deployed via Heroku and is accessible here - https://ci-mp4-shannongaels.herokuapp.com/
 The process for deployment was as follows: Project pushed to GitHub repository Navigated to Settings in relevant GitHub repository Under GitHub Pages, selected relevant branch (master branch) and saved

Local Deployment
Go to directory you would like to clone this project to. Download or clone this link https://github.com/pmadden90/mp4-ecommerce-store and open in your chosen directory.

git clone https://github.com/pmadden90/mp4-ecommerce-store.git

This site is currently deployed on [Heroku](https://www.heroku.com/) using the **master** branch on GitHub. When the project has been setup locally, you can proceed to deploy it remotely with the following steps:

- Create a **requirements.txt** file so Heroku can install the required dependencies to run the app:
    - pip3 freeze --local > requirements.txt`
    - The *requirements.txt* file for this project can be found here: [requirements.txt](project/requirements.txt)
- Create a **Procfile** to tell Heroku what type of application is being deployed using *gunicorn*, and how to run it:
    - web: gunicorn main.wsgi:application > Procfile`
    - The *Procfile* for this project can be found here: [Procfile](project/Procfile)
- Sign up for a free Heroku account, create your project app, and click the **Deploy** tab, at which point you can *Connect GitHub* as the Deployment Method, and select *Enable Automatic Deployment*.

- In the Heroku **Settings** tab, click on the *Reveal Config Vars* button to configure environmental variables. You will need to copy/paste all of the *.env* key value pairs into the config variables, but please omit the *development=1* variable; this is only for local deployment.

## Credits
The login form was sourced from Bootsnipp - https://bootsnipp.com/snippets/vl4R7


### Media
- The photos used in this site were obtained from pexels.com

### Acknowledgements


The page corner folds CSS was from http://nicolasgallagher.com/pure-css-folded-corner-effect/

TravelTim - credited as I have used some of his readme file (from here - https://raw.githubusercontent.com/TravelTimN/ci-milestone05-fsfw/master/README.md) to help write some of the deployment section of this readme.