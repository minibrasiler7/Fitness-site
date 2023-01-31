from flask import Flask, render_template, request, redirect, url_for, flash
from form import LoginForm, RegisterForm, FitnessForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from note_method import *

login_manager = LoginManager()

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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
    ville= db.Column(db.String(250), nullable=False, unique=True)
    url_image = db.Column(db.String(250), nullable=False)
    adresse_url = db.Column(db.String(250), nullable=False)
    note_equipement = db.Column(db.Float(250), nullable=False)
    note_equipement_nombre = db.Column(db.Integer)
    note_personnel = db.Column(db.Float(250))
    note_personnel_nombre = db.Column(db.Integer)
    note_proprete = db.Column(db.Float(250))
    note_proprete_nombre = db.Column(db.Integer)
    is_cours = db.Column(db.Boolean)
    note_cours = db.Column(db.Float(250))
    note_cours_nombre = db.Column(db.Integer)
    is_spa = db.Column(db.Boolean)
    note_spa = db.Column(db.Float(250))
    note_spa_nombre = db.Column(db.Integer)
    prix_mensuel = db.Column(db.Float(250))
    note_general = db.Column(db.Float(250))

    #Optional: this will allow each user object to be identified by its username when printed.
    def __repr__(self):
        return f'<Fitness {self.name}>'

db.create_all()

@app.route("/")
def home():
    fitness_tab = db.session.query(Fitness).all()
    return render_template("index.html",fitness_tab = fitness_tab)


@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user!= None:
            if check_password_hash(user.password, password):
                login_user(user)
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
def log_out():
    logout_user()
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_new():
    form = FitnessForm()
    if request.method == "POST":
        name = request.form.get("fitness_name")
        adresse = request.form.get("adresse").split(", ")[0]
        ville = request.form.get("adresse").split(", ")[1]
        url_image = request.form.get("photo")
        adresse_url = request.form.get("adresse_url")
        is_spa = boolean_reponse(request.form.get("is_spa"))
        is_cours = boolean_reponse(request.form.get("is_cours"))
        if is_spa:
            note_spa = note_to_data(request.form.get("note_spa"))
        if is_cours:
            note_cours = note_to_data(request.form.get("note_cours"))
        note_equipement = note_to_data(request.form.get("note_equipement"))
        note_personnel = note_to_data(request.form.get("note_personnel"))
        note_proprete = note_to_data(request.form.get("note_proprete"))
        prix_mensuel = note_to_data(request.form.get("prix_mensuel"))
        note_equipement_nombre = is_there_note(note_equipement)
        note_personnel_nombre = is_there_note(note_personnel)
        note_cours_nombre = is_there_note(note_cours)
        note_proprete_nombre = is_there_note(note_proprete)
        note_spa_nombre = is_there_note(note_spa)
        note_general = moyenne([note_equipement, note_personnel, note_proprete, note_cours, note_spa])

        fitness =Fitness(
            name=name,
            adresse=adresse,
            ville = ville,
            url_image=url_image,
            adresse_url=adresse_url,
            is_spa=is_spa,
            is_cours=is_cours,
            note_equipement = note_equipement,
            note_equipement_nombre = note_equipement_nombre,
            note_cours = note_cours,
            note_cours_nombre = note_cours_nombre,
            note_personnel = note_personnel,
            note_personnel_nombre = note_personnel_nombre,
            note_proprete = note_proprete,
            note_proprete_nombre = note_proprete_nombre,
            note_spa = note_spa,
            note_spa_nombre = note_spa_nombre,
            prix_mensuel = prix_mensuel,
            note_general = note_general
        )
        db.session.add(fitness)
        db.session.commit()
        return redirect(url_for("home"))

    form = FitnessForm()
    return render_template("add.html", form = form)


if __name__ == "__main__":
    app.run(debug=True)
