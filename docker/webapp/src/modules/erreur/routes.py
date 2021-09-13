import traceback
from flask import Blueprint, render_template
from .. import app

erreur = Blueprint('erreur', __name__, template_folder='templates')

# @erreur.route("<path:invalid_path>")
# def missing(invalid_path):
#     return "There isn't anything at " + invalid_path, 404

@app.errorhandler(404)
def not_found(e):
    print(e)
    print("toto")
    return render_template("erreur.html")


# @app.errorhandler(Exception)
# def general_error(e):
#     print(e)
#     print(traceback.format_exc())
#     return render_template('error.html')

