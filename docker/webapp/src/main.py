from flask import Flask, redirect, request, url_for, render_template
from modules.projects.listprojet import getAllProject

from modules.parametrage import crud

app = Flask(__name__, template_folder='modules')


@app.route("/projects")
def pageListProjets():
    return render_template("projects/list-projet.html", listProjet=getAllProject())


@app.route('/parametrage-cloud', methods=["GET", "POST","PUT"])
def create_bucket():
    """
        Methode permettant la création du bucket
    :return:
    """
    if request.method == "POST":
        data = request.form['namebucket']
        crud.create_bucket_name(data)

    return render_template('parametrage/templates/parametrage.html', bucket_file=crud.get_bucket_name())


if __name__ == "__main__":
    app.run(debug=True)
