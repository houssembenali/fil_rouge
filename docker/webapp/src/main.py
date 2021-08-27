from flask import Flask, redirect, request, url_for, render_template
from flask_login import login_user, current_user, login_required, logout_user
from modules.projects.listprojet import getAllProject
from modules.addproject.addprojet import addProject
import constants as cs
import csv
from _ast import If

from modules.parametrage import crud

app = Flask(__name__, template_folder='modules')


@app.route('/')
def index():
    return render_template('login/templates/index.html', current_user="")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('pageListProjets'))
    return render_template('login/templates/login.html', error=error, current="login", current_user="")

@app.route("/projects")
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
    return render_template("projects/list-projet.html", message=msg,error=errorMsg, current_user="admin", current="list",listProjet=getAllProject())


@app.route("/addproject")
@login_required
def pageAddProjet():
    return render_template("addproject/add-projet.html",current="add")


@app.route('/api/addrepo', methods=['POST'])
@login_required
def addRepo():
    errorMsg = ""
    errorMsg=addProject(request.form)
    return redirect(url_for(".pageListProjets" , current="list", current_user="admin", message = request.form['name'],error=errorMsg,listProjet=getAllProject()))

@app.route('/parametrage-cloud', methods=["GET", "POST","PUT"])
@login_required
def create_bucket():
    """
        Methode permettant la création du bucket
    :return:
    """
    if request.method == "POST":
       data = request.form['namebucket']
       crud.create_bucket_name(data)

    return render_template('parametrage/templates/parametrage.html', bucket_file=crud.get_bucket_name(), current="param")

@app.route('/logout')
@login_required
def logout():
    user = current_user
    logout_user()
    return render_template('login/templates/index.html')

if __name__ == "__main__":
    app.run(debug=True)
    login = LoginManager()
    login.login_view = "users.login"

