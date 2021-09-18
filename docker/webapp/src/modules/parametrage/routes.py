#################
#### imports ####
#################

from flask import Blueprint, request, render_template
from flask_login import login_required

from modules.parametrage import crud

parametrage_blueprint = Blueprint('parametrage', __name__, template_folder='templates')


################
#### routes ####
################

@parametrage_blueprint.route('/')
@login_required
def parametrage():
    return render_template('parametrage.html', sucess=False)
    
@parametrage_blueprint.route('/parametrage-cloud', methods=["GET", "POST","PUT"])
@login_required
def create_bucket():
    """
        Methode permettant la création du bucket
    :return:
    """
    suc=False
    if request.method == "POST":
       data = request.form['namebucket']
       updated = request.form['updated']
       if updated == "1":
            suc=True
       crud.create_bucket_name(data)
    return render_template('parametrage.html', bucket_file=crud.get_bucket_name(), current="param",sucess=suc)
