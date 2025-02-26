from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///treasure.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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
