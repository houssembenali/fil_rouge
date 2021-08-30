#################
#### imports ####
#################

from flask import Flask, Blueprint, redirect, request, url_for, render_template
from flask_login import login_required
from modules.projects.listprojet import getAllProject
from modules.addproject.addprojet import addProject
import csv
from _ast import If

projects_blueprint = Blueprint('projects', __name__, template_folder='templates')


################
#### routes ####
################

@projects_blueprint.route("/projects")
@login_required
def pageListProjets():
    if 'message' in request.args:
        msg=request.args.get("message")
    else:
        msg=""
    
    if 'error' in request.args:
        errorMsg=request.args.get("error")
    else:
        errorMsg=""
    return render_template("list-projet.html", message=msg,error=errorMsg, current="list",listProjet=getAllProject())