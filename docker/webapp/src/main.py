from flask import Flask, redirect, request, url_for, render_template
from modules.projects.listprojet import getAllProject
from modules.addproject.addprojet import addProject
import constants as cs
import csv
from _ast import If

from modules.parametrage import crud

app = Flask(__name__, template_folder='modules')


@app.route("/webhook", methods=["POST"])
def pageListProjets():
    print (request.data)
    jsondata = json.loads(request.data)
    print ("full_name: {}".format(jsondata['repository']['full_name']))
    print ("html_url: {}.git".format(jsondata['repository']['html_url']))
    print ("New commit by: {}".format(jsondata['commits'][0]['author']['name']))
    return (request.data)


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
    return redirect(url_for(".pageListProjets" , current="list", message = request.form['name'],error=errorMsg,listProjet=getAllProject()))

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
