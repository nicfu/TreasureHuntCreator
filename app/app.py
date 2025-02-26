from flask import Flask, render_template, session
from auth import auth_bp
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///treasure.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return render_template("index.html")\

@app.route("/health")
def health():
    return "{status: 'ok'}"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
