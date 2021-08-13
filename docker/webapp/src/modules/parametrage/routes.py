#################
#### imports ####
#################

from flask import Flask, redirect, request, url_for, render_template
from flask_login import login_required
# from modules.projects.listprojet import getAllProject
# from modules.addproject.addprojet import addProject
# import constants as cs
import csv
from _ast import If

from modules.parametrage import crud

from . import parametrage_blueprint


################
#### routes ####
################

@parametrage_blueprint.route('/')
@login_required
def parametrage():
    return render_template('parametrage.html')
    
@parametrage_blueprint.route('/parametrage-cloud', methods=["GET", "POST"])
@login_required
def create_bucket():
    if request.method == "POST":
       data = request.form['namebucket']
       crud.create_bucket_name(data)

    return render_template('parametrage.html', bucket_file=crud.get_bucket_name(), current="param")
