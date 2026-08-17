import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from mongoengine import connect

from routes.admin import admin
from routes.index import index
from routes.login import login_blueprint
from schema.index import users

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
connect(host=os.getenv("MONGO_URI"), uuidRepresentation="standard")

#LOGIN
login_manager = LoginManager(app)
login_manager.login_view = "index.first_page"
@login_manager.user_loader
def load_user(user_id):
    user = users.objects(id=user_id).first()
    if user:
        return user
    else:
        return None

#ROUTES
app.register_blueprint(index)
app.register_blueprint(login_blueprint)
app.register_blueprint(admin, url_prefix="/admin")


# for rule in app.url_map.iter_rules():
#     print(rule)

if __name__ == "__main__":
    app.run(debug=True)