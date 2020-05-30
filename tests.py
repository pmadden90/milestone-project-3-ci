# project/test_basic.py
from app import app
import os
import unittest
from os import path
#if path.exists("../app.py"):
#    import app
from wtforms.ext.appengine import db
#import app
 

 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
       app.config['TESTING'] = True
       app.config['WTF_CSRF_ENABLED'] = False
       app.config['DEBUG'] = False
        
       self.app = app.test_client()
        

 
        # Disable sending emails during unit testing
        #mail.init_app(app)
        #self.assertEqual(app.debug, False)
 
    # executed after each test
    #def tearDown(self):
     #   pass
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_page(self):
        response = self.app.get('/recipes', follow_redirects=True)
        print(response.data)
        self.assertEqual(response.status_code, 200)

    #def test_new_recipe():

        

if __name__ == "__main__":
    unittest.main()