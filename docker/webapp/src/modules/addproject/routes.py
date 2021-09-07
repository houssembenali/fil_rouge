#################
#### imports ####
#################

from flask import Blueprint, redirect, request, url_for, render_template
from flask_login import login_required
from modules.projects.listprojet import get_all_projects, publish_from_file_by_id
from modules.addproject import addprojet
from utils import delete_from_file_by_id
import constants as cs
import wordings

addproject_blueprint = Blueprint('addproject', __name__, template_folder='templates')

PROJECTS_PAGE_LIST_PROJETS = "projects.page_list_projets"

################
#### routes ####
################ 

@addproject_blueprint.route("/addproject")
@login_required
def page_add_projet():
    return render_template("add-projet.html",current="add")


@addproject_blueprint.route('/api/addrepo', methods=['POST'])
@login_required
def add_repo():
    errormsg = ""
    errormsg = addprojet.add_project(request.form)
    msg= wordings.PROJET_AJOUTE_SUCCES.format(name=request.form['name'])
    return redirect(url_for(PROJECTS_PAGE_LIST_PROJETS , current="list", message = msg,error=errormsg,listProjet=get_all_projects()))

@addproject_blueprint.route('/api/delrepo', methods=['POST'])
@login_required
def delete_repo():
    errormsg = ""
    errormsg=delete_from_file_by_id(request.form["id"],cs.PROJECT_FILE_PATH)
    msg = wordings.PROJET_SUPPRIME_SUCCES.format(name=request.form['name'])
    return redirect(url_for(PROJECTS_PAGE_LIST_PROJETS , current="list", message = msg,error=errormsg,listProjet=get_all_projects()))

@addproject_blueprint.route('/api/pubrepo', methods=['POST'])
@login_required
def publish_repo():
    errormsg = ""
    has_summary = False
    if "sommaire" in request.form:
        has_summary=True
    errormsg = publish_from_file_by_id(request.form["id"],request.form["name"],request.form["link"],has_summary)
    msg = wordings.PROJET_PUBLIE_SUCCES.format(name=request.form['name'])
    return redirect(url_for(PROJECTS_PAGE_LIST_PROJETS , current="list", message = msg,error=errormsg,listProjet=get_all_projects()))