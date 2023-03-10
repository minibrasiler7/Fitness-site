import flask_login
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from form import LoginForm, RegisterForm, FitnessForm, CommentaireForm, ContactForm, Updateform
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from note_method import *
from flask_ckeditor import CKEditor
import datetime
from html import unescape
import smtplib
from functools import wraps
import os

login_manager = LoginManager()

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "sqlite:///fitness.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',"dlkjwnefooinwnef")
login_manager.init_app(app)
ckeditor = CKEditor(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if flask_login.current_user.id != 1:
            return redirect(url_for('home', next=request.url))
        return f(*args, **kwargs)
    return decorated_function



##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///fitness.db"

#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

##CREATE TABLE
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    #Optional: this will allow each user object to be identified by its username when printed.
    def __repr__(self):
        return f'<User {self.username}>'

class Fitness(db.Model):
    __tablename__ = 'fitness'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    adresse = db.Column(db.String(250), nullable=False, unique=True)
    site_url = db.Column(db.String(250), nullable=False, unique=True)
    ville= db.Column(db.String(250), nullable=False)
    code_postal = db.Column(db.Integer)
    url_image = db.Column(db.String(250), nullable=False)
    adresse_url = db.Column(db.String(250), nullable=False)
    note_equipement = db.Column(db.Float(250))
    note_equipement_nombre = db.Column(db.Integer)
    note_personnel = db.Column(db.Float(250))
    note_personnel_nombre = db.Column(db.Integer)
    note_piscine = db.Column(db.Float(250))
    note_piscine_nombre = db.Column(db.Integer)
    note_proprete = db.Column(db.Float(250))
    note_proprete_nombre = db.Column(db.Integer)
    is_cours = db.Column(db.Boolean)
    note_cours = db.Column(db.Float(250))
    note_cours_nombre = db.Column(db.Integer)
    is_spa = db.Column(db.Boolean)
    is_piscine = db.Column(db.Boolean)
    note_spa = db.Column(db.Float(250))
    note_spa_nombre = db.Column(db.Integer)
    prix_mensuel = db.Column(db.Float(250))
    note_general = db.Column(db.Float(250))
    note_general_nombre = db.Column(db.Float(250))
    lundi_ouverture = db.Column(db.String(250), nullable=False)
    mardi_ouverture = db.Column(db.String(250), nullable=False)
    mercredi_ouverture = db.Column(db.String(250), nullable=False)
    jeudi_ouverture = db.Column(db.String(250), nullable=False)
    vendredi_ouverture = db.Column(db.String(250), nullable=False)
    samedi_ouverture = db.Column(db.String(250), nullable=False)
    dimanche_ouverture = db.Column(db.String(250), nullable=False)

    #Optional: this will allow each user object to be identified by its username when printed.
    def __repr__(self):
        return f'<Fitness {self.name}>'

class Note_user_fitness(db.Model, UserMixin):
    __tablename__ = 'noteuserfitness'
    id = db.Column(db.Integer, primary_key= True)
    id_fitness = db.Column(db.Integer, nullable=False)
    id_user = db.Column(db.Integer, nullable = False)
    #Optional: this will allow each user object to be identified by its username when printed.
    def __repr__(self):
        return f'<User {self.username}>'

class Commentaire(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    id_fitness = db.Column(db.Integer, nullable=False)
    id_user = db.Column(db.Integer, nullable= False)
    name_user = db.Column(db.String(250), nullable=False)
    name_fitness= db.Column(db.String(250), nullable=False)
    commentaire = db.Column(db.String(450), nullable=False)
    date = db.Column(db.String(450), nullable=False)

db.create_all()

def jours_horaire(jour_debut, jour_fin):
    if jour_debut=="ferm??" or jour_fin=="24/24":
        return jour_debut
    else:
        return f"{jour_debut} - {jour_fin}"

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
            data = request.form.get("recherche").title()
            fitness_tab = Fitness.query.filter_by(ville=data).all()
            if len(fitness_tab) == 0 :
                fitness_tab= Fitness.query.filter_by(code_postal=data).all()
                if len(fitness_tab) == 0 :
                    fitness_tab= Fitness.query.filter_by(name=data).all()

            return render_template("index.html",fitness_tab = fitness_tab, appreciation=appreciation, h2=data)
    fitness_tab = db.session.query(Fitness).all()
    return render_template("index.html",fitness_tab = fitness_tab, appreciation=appreciation)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user!= None:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                session['username'] = user.username
                return redirect(url_for('home'))
            else:
                flash("Sorry you password is not correct please try again...")
                return redirect(url_for('login'))
        else:
            flash("Sorry we didn't find you.")
            return redirect(url_for('login'))
    return render_template("login.html", form = form)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method =="POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        hash = generate_password_hash(method="pbkdf2:sha256", salt_length=8, password=password)
        user = User(
            username = username,
            email = email,
            password = hash
        )
        if User.query.filter_by(email=email).first() == None:
            db.session.add(user)
            db.session.commit()
            flash('You were successfully Register')
            return redirect(url_for("home"))
        else:
            flash('You have already an account please log in')
            return redirect(url_for("login"))

    form = RegisterForm()
    return render_template("register.html", form = form)

@app.route("/log_out")
@login_required
def log_out():
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for("home"))

@app.route("/info")
def info():
    id = request.args.get("id")
    fitness = Fitness.query.filter_by(id=id).first()
    commentaires = Commentaire.query.filter_by(id_fitness=fitness.id)
    return render_template("info.html", fitness=fitness, commentaires = commentaires)
@app.route("/add", methods=["GET", "POST"])
@admin_required
def add_new():
    form = FitnessForm()
    if request.method == "POST":
        name = request.form.get("fitness_name")
        adresse = request.form.get("adresse").split(", ")[0]
        code_postal = request.form.get("adresse").split(", ")[1].split(" ")[0]
        ville = request.form.get("adresse").split(", ")[1].split(" ")[1]
        url_image = request.form.get("photo")
        site_url = request.form.get("site_url")
        adresse_url = request.form.get("adresse_url")
        is_spa = boolean_reponse(request.form.get("is_spa"))
        is_cours = boolean_reponse(request.form.get("is_cours"))
        is_piscine = boolean_reponse(request.form.get("is_piscine"))
        note_piscine = None
        note_spa=None
        note_cours = None
        if is_spa:
            note_spa = note_to_data(request.form.get("note_spa"))
        if is_cours:
            note_cours = note_to_data(request.form.get("note_cours"))
        if is_piscine:
            note_piscine = note_to_data(request.form.get("note_piscine"))
        note_equipement = note_to_data(request.form.get("note_equipement"))
        note_piscine = note_to_data(request.form.get("note_piscine"))
        note_personnel = note_to_data(request.form.get("note_personnel"))
        note_proprete = note_to_data(request.form.get("note_proprete"))
        prix_mensuel = float(request.form.get("prix_mensuel"))
        note_equipement_nombre = is_there_note(note_equipement)
        note_personnel_nombre = is_there_note(note_personnel)
        note_cours_nombre = is_there_note(note_cours)
        note_piscine_nombre = is_there_note(note_piscine)
        note_proprete_nombre = is_there_note(note_proprete)
        note_spa_nombre = is_there_note(note_spa)
        note_general = moyenne([note_equipement, note_personnel, note_proprete, note_cours, note_spa])
        note_general_nombre= is_there_note(note_general)

        lundi_ouverture = jours_horaire(request.form.get("lundi_ouverture"),request.form.get("lundi_fermeture"))
        mardi_ouverture = jours_horaire(request.form.get("mardi_ouverture"),request.form.get("mardi_fermeture"))
        mercredi_ouverture = jours_horaire(request.form.get("mercredi_ouverture"),request.form.get("mercredi_fermeture"))
        jeudi_ouverture = jours_horaire(request.form.get("jeudi_ouverture"),request.form.get("jeudi_fermeture"))
        vendredi_ouverture = jours_horaire(request.form.get("vendredi_ouverture"),request.form.get("vendredi_fermeture"))
        samedi_ouverture = jours_horaire(request.form.get("samedi_ouverture"),request.form.get("samedi_fermeture"))
        dimanche_ouverture = jours_horaire(request.form.get("dimanche_ouverture"),request.form.get("dimanche_fermeture"))


        fitness = Fitness(
            name=name,
            adresse=adresse,
            ville = ville,
            url_image=url_image,
            site_url = site_url,
            adresse_url=adresse_url,
            code_postal=code_postal,
            is_spa=is_spa,
            is_cours=is_cours,
            is_piscine = is_piscine,
            note_equipement = note_equipement,
            note_equipement_nombre = note_equipement_nombre,
            note_cours = note_cours,
            note_cours_nombre = note_cours_nombre,
            note_personnel = note_personnel,
            note_personnel_nombre = note_personnel_nombre,
            note_proprete = note_proprete,
            note_proprete_nombre = note_proprete_nombre,
            note_spa = note_spa,
            note_piscine=note_piscine,
            note_piscine_nombre=note_piscine_nombre,
            note_spa_nombre = note_spa_nombre,
            prix_mensuel = prix_mensuel,
            note_general = note_general,
            note_general_nombre = note_general_nombre,
            lundi_ouverture = lundi_ouverture,
            mardi_ouverture = mardi_ouverture,
            mercredi_ouverture = mercredi_ouverture,
            jeudi_ouverture = jeudi_ouverture,
            vendredi_ouverture = vendredi_ouverture,
            samedi_ouverture = samedi_ouverture,
            dimanche_ouverture = dimanche_ouverture
        )
        db.session.add(fitness)
        db.session.commit()
        return redirect(url_for("home"))

    form = FitnessForm()
    return render_template("add.html", form = form)

@app.route("/commenter", methods = ["GET", "POST"])
def commenter():
    id = request.args.get("id_fitness")
    fitness = Fitness.query.filter_by(id=id).first()
    form = CommentaireForm()
    if request.method == "POST":
        commentaire = unescape(request.form.get("ckeditor")[3:-4])
        id_fitness = id
        name_fitness = fitness.name
        user_id = flask_login.current_user.id
        user_name = flask_login.current_user.username
        date = datetime.datetime.now()
        if date.day <10:
            jour = f"0{date.day}"
        else:
            jour = date.day
        if date.month <10:
            mois = f"0{date.month}"
        else:
            mois = date.month
        year = date.year
        date_reformated = f"{jour}/{mois}/{year}"
        if len(commentaire)>0:
            comment = Commentaire(
                id_fitness=id_fitness,
                name_fitness=name_fitness,
                id_user=user_id,
                name_user =user_name,
                commentaire=commentaire,
                date = date_reformated
            )
            db.session.add(comment)
            db.session.commit()
            flash("F??licitation votre commentaire a ??t?? enregistr??!")

        check_nombre_comment = len(Note_user_fitness.query.filter_by(id_fitness=fitness.id, id_user=user_id).all())
        if check_nombre_comment<1:
            note_equipement = note_to_data(request.form.get("note_equipement"))
            note_personnel = note_to_data(request.form.get("note_personnel"))
            note_proprete = note_to_data(request.form.get("note_proprete"))
            note_spa=None
            if fitness.is_spa:
                note_spa = note_to_data(request.form.get("note_spa"))
            note_cours =None
            if fitness.is_cours:
                note_cours = note_to_data(request.form.get("note_cours"))
            new_notes = {"note_equipement": note_equipement,
                         "note_personnel": note_personnel,
                         "note_proprete": note_proprete,
                         "note_spa": note_spa,
                         "note_cours":note_cours}
            old_notes = {"note_equipement": [fitness.note_equipement, fitness.note_equipement_nombre],
                         "note_personnel": [fitness.note_personnel, fitness.note_personnel_nombre],
                         "note_proprete": [fitness.note_proprete, fitness.note_proprete_nombre],
                         "note_spa": [fitness.note_spa, fitness.note_spa_nombre],
                         "note_cours": [fitness.note_cours, fitness.note_cours_nombre]}

            averages_notes = update_moyenne(old_notes,new_notes)
            averages_notes_tab = [item[0] for (key,item) in averages_notes.items()]


            if note_equipement!=None or note_cours!=None or note_spa!=None or note_personnel!=None or note_proprete!=None:
                fitness.note_general_nombre += 1
                fitness.note_equipement = averages_notes['note_equipement'][0]
                fitness.note_equipement_nombre = averages_notes['note_equipement'][1]
                fitness.note_personnel = averages_notes['note_personnel'][0]
                fitness.note_personnel_nombre= averages_notes['note_personnel'][1]
                fitness.note_proprete = averages_notes['note_proprete'][0]
                fitness.note_proprete_nombre= averages_notes['note_proprete'][1]
                fitness.note_spa = averages_notes['note_spa'][0]
                fitness.note_spa_nombre= averages_notes['note_spa'][1]
                fitness.note_cours = averages_notes['note_cours'][0]
                fitness.note_cours_nombre= averages_notes['note_cours'][1]
                fitness.note_general= moyenne(averages_notes_tab)
                note_user_fitness = Note_user_fitness(id_fitness = fitness.id,
                                  id_user = user_id
                                  )
                db.session.add(note_user_fitness)
                db.session.commit()
            return redirect(url_for('home'))
        else:
            flash("Vous avez d??j?? donn?? votre avis sur ce fitness")
            return redirect(url_for("home"))


    return render_template("commenter.html", fitness=fitness, form = form)

@app.route("/contact", methods = ["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        nom = request.form.get("nom")
        email = request.form.get("email")
        adresse = request.form.get("adresse")
        ville = request.form.get("ville")
        is_piscine = request.form.get("is_piscine")
        is_cours = request.form.get("is_cours")
        is_spa = request.form.get("is_spa")
        commentaire = unescape(request.form.get("ckeditor")[3:-4])
        message = f"Nouveau fitness ?? ajouter \n " \
                  f"Nom: {nom} \n" \
                  f"Email du propri??taire: {email} \n" \
                  f"Adresse du fitness: {adresse} \n" \
                  f"Ville : {ville}\n" \
                  f"Piscine? : {is_piscine}\n" \
                  f"Cours? : {is_cours}\n" \
                  f"SPA? : {is_spa}\n" \
                  f"Commentaire?: {commentaire}"

        smtp_server = "smtp.gmail.com"
        to_adr = "loic_Strauch_19@msn.com"
        from_adr = "loicstrauch123@gmail.com"
        password = "vouelukgzkutyvji"
        print(message)

        with smtplib.SMTP_SSL(smtp_server) as connection:
            connection.login(from_adr, password)
            connection.sendmail(from_addr=from_adr,
                                to_addrs=to_adr,
                                msg= f"Subject: New fitness! \n\n {message}".encode('utf-8'))
        flash("Votre email a ??t?? envoy?? ?? l'administrateur du site!")
        return redirect(url_for("home"))


    return render_template("contact.html", form = form)

@app.route("/delete", methods = ["GET", "POST"])
@admin_required
def delete():
    id = request.args.get("id_fitness")
    fitness = Fitness.query.filter_by(id=id).first()
    commentaires = Commentaire.query.filter_by(id_fitness = id).all()
    print(commentaires)
    notes_user_fitness = Note_user_fitness.query.filter_by(id_fitness = id).all()
    for commentaire in commentaires:
        db.session.delete(commentaire)
    for note_user_fitness in notes_user_fitness:
        db.session.delete(note_user_fitness)
    db.session.delete(fitness)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update", methods = ["GET", "POST"])
@admin_required
def update():
    id = request.args.get("id_fitness")
    form = Updateform()
    if request.method == "POST":
        fitness = Fitness.query.filter_by(id=id).first()
        fitness.name = form.nom.data
        fitness.site_url = form.url_site.data
        fitness.adresse = form.adresse.data
        fitness.adresse_url = form.url_map.data
        fitness.url_image = form.url_image.data
        fitness.is_spa = form.is_spa.data
        fitness.is_piscine = form.is_piscine.data
        fitness.is_cours = form.is_cours.data
        fitness.code_postal = form.code_postal.data
        fitness.ville = form.ville.data
        db.session.commit()
        return redirect(url_for("home"))


    fitness = Fitness.query.filter_by(id=id).first()
    form.is_piscine.data = fitness.is_piscine
    form.url_site.data = fitness.site_url
    form.url_image.data = fitness.url_image
    form.url_map.data = fitness.adresse_url
    form.is_spa.data = fitness.is_spa
    form.is_cours.data = fitness.is_cours
    form.nom.data = fitness.name
    form.adresse.data = fitness.adresse
    form.code_postal.data = fitness.code_postal
    form.ville.data = fitness.ville
    return render_template("update.html", form=form, fitness=fitness)



if __name__ == "__main__":
    app.run(debug=True)




