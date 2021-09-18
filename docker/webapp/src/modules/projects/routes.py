#################
#### imports ####
#################

from flask import Blueprint, request, render_template
from flask_login import login_required
from modules.projects.listprojet import get_all_projects

projects_blueprint = Blueprint('projects', __name__, template_folder='templates')


################
#### routes ####
################

@projects_blueprint.route("/projects")
@login_required
def page_list_projets():
    if 'message' in request.args:
        msg=request.args.get("message")
    else:
        msg=""
    
    if 'error' in request.args:
        errormsg=request.args.get("error")
    else:
        errormsg=""
    return render_template("list-projet.html", message=msg,error=errormsg, current="list",listProjet=get_all_projects())