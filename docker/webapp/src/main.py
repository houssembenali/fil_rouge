from flask import Flask, redirect, request, url_for, render_template
import constants as cs
import csv
from _ast import If
from modules.projects.listprojet import getAllProject
from modules.addproject.addprojet import addProject
from modules.parametrage import crud
from utils import deleteFromFileById



app = Flask(__name__, template_folder='modules')

@app.route("/")
def index():
    return pageListProjets()


@app.route("/projects")
def pageListProjets():
    if 'message' in request.args:
        msg=request.args.get("message")
    else:
        msg=""
    
    if 'error' in request.args:
        errorMsg=request.args.get("error")
    else:
        errorMsg=""
    return render_template("projects/list-projet.html", message=msg,error=errorMsg, current="list",listProjet=getAllProject())


@app.route("/addproject")
def pageAddProjet():
    return render_template("addproject/add-projet.html",current="add")


@app.route('/api/addrepo', methods=['POST'])
def addRepo():
    errorMsg = ""
    errorMsg=addProject(request.form)
    msg= "Le projet «" + request.form['name'] + "» est ajouté avec succès."
    return redirect(url_for(".pageListProjets" , current="list", message = msg,error=errorMsg,listProjet=getAllProject()))

@app.route('/api/delrepo', methods=['POST'])
def deleteRepo():
    errorMsg = ""
    errorMsg=deleteFromFileById(request.form["id"],cs.PROJECT_FILE_PATH)
    msg = "Le projet «" + request.form['name'] + "» est supprimé avec succès."
    return redirect(url_for(".pageListProjets" , current="list", message = msg,error=errorMsg,listProjet=getAllProject()))


@app.route('/parametrage-cloud', methods=["GET", "POST","PUT"])
def create_bucket():
    """
        Methode permettant la création du bucket
    :return:
    """
    if request.method == "POST":
       data = request.form['namebucket']
       crud.create_bucket_name(data)

    return render_template('parametrage/templates/parametrage.html', bucket_file=crud.get_bucket_name(), current="param")

if __name__ == "__main__":
    app.run(debug=True)
