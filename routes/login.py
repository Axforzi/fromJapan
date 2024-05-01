from flask import Blueprint, redirect, render_template, flash
from flask_login import current_user, logout_user
from services.admin import login_service

login_blueprint = Blueprint("login", __name__)

@login_blueprint.route("/login", methods=["GET"])
def login_page():
    if current_user.is_authenticated:
        return redirect("/admin")
    else:
        return render_template('pages/admin/login.html')

@login_blueprint.route("/login", methods=["POST"])
def login():
    if login_service():
        return redirect('/admin')
    else:
        return render_template("pages/admin/login.html")
        
@login_blueprint.route("/logout")
def logout_website():
    logout_user()
    return redirect("/")