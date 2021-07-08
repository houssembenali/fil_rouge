from flask import Flask, redirect, url_for, render_template
from modules.projects.listprojet import getAllProject

app = Flask(__name__, template_folder='modules')


@app.route("/projects")
def pageListProjets():
    return render_template("projects/list-projet.html", listProjet=getAllProject())





if __name__ == "__main__":
    app.run(debug=True)
