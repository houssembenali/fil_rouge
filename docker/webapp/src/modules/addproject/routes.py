#################
#### imports ####
#################

from flask import Flask, Blueprint, redirect, request, url_for, render_template
from flask_login import login_required
from modules.projects.listprojet import getAllProject
from modules.addproject import addprojet
import csv
from _ast import If

addproject_blueprint = Blueprint('addproject', __name__, template_folder='templates')


################
#### routes ####
################

@addproject_blueprint.route("/addproject")
@login_required
def pageAddProjet():
    return render_template("add-projet.html",current="add")


@addproject_blueprint.route('/api/addrepo', methods=['POST'])
@login_required
def addRepo():
    errorMsg = ""
    
    errorMsg=addProject(request.form)
    return redirect(url_for(".pageListProjets" , current="list", message = request.form['name'],error=errorMsg,listProjet=getAllProject()))
