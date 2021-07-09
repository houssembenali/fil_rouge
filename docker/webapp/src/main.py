from flask import Flask, redirect, request, url_for, render_template

from modules.projects.listprojet import getAllProject
from modeles import ParamBucket
from modules.parametrage import crud

app = Flask(__name__, template_folder='modules')

@app.route("/")
def hello_world():
    return "Bienvenue sur l'application fil rouge"

@app.route('/parametrage-cloud', methods=["GET", "POST","PUT"])
def create_bucket():
    
    if request.method == "POST":
        data = request.form['namebucket']
        #bucket = ParamBucket(data)
        crud.create_bucket_name(data)

    # if request.method == "PUT":
    #     data = request.form['namebucket']
    #     crud.update_bucket_by_name(data)

    return render_template('parametrage/templates/parametrage.html')


@app.route("/projects")
def pageListProjets():
    return render_template("projects/list-projet.html", listProjet=getAllProject())


if __name__ == "__main__":
    app.run(debug=True)