from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/projects")
def pageListProjets():
    return render_template("list-projet.html", listProjet=getAllProject())


def getAllProject():
    list_projets=[]

    f = open("DB/projects.txt", "r")
    Lines = f.readlines()
    count = 0
    for line in Lines:
        count += 1
        list_projets.append(line.split(";"))
    return list_projets



if __name__ == "__main__":
    app.run(debug=True)
