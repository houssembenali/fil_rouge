#################
#### imports ####
#################

from flask import Flask, Blueprint, redirect, request, url_for, render_template
from flask_login import login_required
from modules.projects.listprojet import getAllProject, publishFromFileById
from modules.addproject import addprojet
from utils import deleteFromFileById
import csv
import constants as cs
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
    errorMsg=addprojet.addProject(request.form)
    msg= "Le projet «" + request.form['name'] + "» est ajouté avec succès."
    return redirect(url_for("projects.pageListProjets" , current="list", message = msg,error=errorMsg,listProjet=getAllProject()))

@addproject_blueprint.route('/api/delrepo', methods=['POST'])
@login_required
def deleteRepo():
    errorMsg = ""
    errorMsg=deleteFromFileById(request.form["id"],cs.PROJECT_FILE_PATH)
    msg = "Le projet «" + request.form['name'] + "» est supprimé avec succès."
    return redirect(url_for("projects.pageListProjets" , current="list", message = msg,error=errorMsg,listProjet=getAllProject()))

@addproject_blueprint.route('/api/pubrepo', methods=['POST'])
@login_required
def publishRepo():
    errorMsg = ""
    isSommaire = False
    if "sommaire" in request.form:
        isSommaire=True
    errorMsg=publishFromFileById(request.form["id"],request.form["name"],request.form["link"],isSommaire)
    msg = "Le projet «" + request.form['name'] + "» est publié avec succès."
    return redirect(url_for("projects.pageListProjets" , current="list", message = msg,error=errorMsg,listProjet=getAllProject()))