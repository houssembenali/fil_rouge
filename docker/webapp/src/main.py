from flask import Flask, redirect, url_for, render_template,request
from modules.projects.listprojet import getAllProject
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
    resultat = request.form
    nom = resultat['name']
    link = resultat['link']

    
    max = 1
    with open(cs.PROJECT_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        
        for row in csv_reader:
            if max < int(list({row[0]})[0]):
               max=int(list({row[0]})[0])
           
    
    
    max=max+1
    
    with open(cs.PROJECT_FILE_PATH, mode='a',newline='') as projects_file:
        projects_writer = csv.writer(projects_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        projects_writer.writerow([max,nom,link])
    
    
    #return render_template("projects/list-projet.html" , current="list", message = nom,listProjet=getAllProject())
    return redirect(url_for(".pageListProjets" , current="list", message = nom,listProjet=getAllProject()))

if __name__ == "__main__":
    app.run(debug=True)
