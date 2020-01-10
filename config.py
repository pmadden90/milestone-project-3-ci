import os

# Config settings and environment variables
class Config:
    MONGO_DBNAME = 'recipes_db'
    MONGO_URI = os.getenv("MONGO_URI")
    SECRET_KEY = os.getenv("'mongodb+srv://root:recipespc90@myfirstcluster-8qt4w.mongodb.net/recipes_db?retryWrites=true&w=majority'")