from flask import Flask, redirect, request, url_for, render_template
import constants as cs
import csv
from _ast import If
from modules.projects.listprojet import getAllProject
from modules.projects.listprojet import publishFromFileById
from modules.addproject.addprojet import addProject
from modules.parametrage import crud
from utils import deleteFromFileById
import logging, logging.config

app = Flask(__name__, template_folder='modules')
#initialisation logger
logging.config.fileConfig('logconfig.ini')
logger=logging.getLogger()


@app.route("/")
def index():
    return pageListProjets()


@app.route("/projects")
def pageListProjets():
    logger.info("Debut chargement de la liste des projets")
    if 'message' in request.args:
        msg=request.args.get("message")
    else:
        msg=""
    
    if 'error' in request.args:
        errorMsg=request.args.get("error")
        logger.error(errorMsg)
    else:
        errorMsg=""
    logger.info("Fin chargement liste des projets")
    return render_template("projects/list-projet.html", message=msg,error=errorMsg, current="list",listProjet=getAllProject())


@app.route("/addproject")
def pageAddProjet():
    logger.info("Chargement page ajout projet")
    return render_template("addproject/add-projet.html",current="add")


@app.route('/api/addrepo', methods=['POST'])
def addRepo():
    logger.info("Debut ajout du projet"+request.form['name'])
    errorMsg = ""
    errorMsg=addProject(request.form)
    if errorMsg != "":
        logger.error(errorMsg)
    msg= "Le projet «" + request.form['name'] + "» est ajouté avec succès."
    logger.info("Fin ajout du projet"+request.form['name'])
    return redirect(url_for(".pageListProjets" , current="list", message = msg,error=errorMsg,listProjet=getAllProject()))

@app.route('/api/delrepo', methods=['POST'])
def deleteRepo():
    logger.info("Debut suppression du projet"+request.form['name'])
    errorMsg = ""
    errorMsg=deleteFromFileById(request.form["id"],cs.PROJECT_FILE_PATH)
    if errorMsg != "":
        logger.error(errorMsg)
    msg = "Le projet «" + request.form['name'] + "» est supprimé avec succès."
    logger.info("Fin suppression du projet"+request.form['name'])
    return redirect(url_for(".pageListProjets" , current="list", message = msg,error=errorMsg,listProjet=getAllProject()))

@app.route('/api/pubrepo', methods=['POST'])
def publishRepo():
    logger.info("Debut publication du projet"+request.form['name'])
    errorMsg = ""
    isSommaire = False
    if "sommaire" in request.form:
        isSommaire=True
    errorMsg=publishFromFileById(request.form["id"],request.form["name"],request.form["link"],isSommaire)
    if errorMsg != "":
        logger.error(errorMsg)
    msg = "Le projet «" + request.form['name'] + "» est publié avec succès."
    logger.info("Fin publication du projet"+request.form['name'])
    return redirect(url_for(".pageListProjets" , current="list", message = msg,error=errorMsg,listProjet=getAllProject()))


@app.route('/parametrage-cloud', methods=["GET", "POST","PUT"])
def create_bucket():
    """
        Methode permettant la création du bucket
    :return:
    """
    logger.info("Paramétrage nom bucket")
    if request.method == "POST":
       data = request.form['namebucket']
       crud.create_bucket_name(data)

    return render_template('parametrage/templates/parametrage.html', bucket_file=crud.get_bucket_name(), current="param")

if __name__ == "__main__":
    app.run(debug=True)
