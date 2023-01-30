from flask import Flask, render_template, request, redirect, url_for, flash
from form import LoginForm, RegisterForm, FitnessForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user

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
#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

##CREATE TABLE
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    #Optional: this will allow each user object to be identified by its username when printed.
    def __repr__(self):
        return f'<User {self.username}>'

db.create_all()

@app.route("/")
def home():
    return render_template("index.html")


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

@app.route("/add")
def add_new():
    form = FitnessForm()
    return render_template("add.html", form = form)




if __name__ == "__main__":
    app.run(debug=True)
