from flask import Flask, redirect, url_for, render_template,request
from modules.projects.listprojet import getAllProject
from modules.addproject.addprojet import addProject
import constants as cs
import csv
from _ast import If

app = Flask(__name__, template_folder='modules')


@app.route("/projects")
def pageListProjets():
    if 'message' in request.args:
        msg=request.args.get("message")
    else:
        msg=""
    
    return render_template("projects/list-projet.html", message=msg, current="list",listProjet=getAllProject())


@app.route("/addproject")
def pageAddProjet():
    return render_template("addproject/add-projet.html",current="add")



@app.route('/api/addrepo', methods=['POST'])
def addRepo():
    addProject(request.form)
    return redirect(url_for(".pageListProjets" , current="list", message = request.form['name'],listProjet=getAllProject()))

if __name__ == "__main__":
    app.run(debug=True)
