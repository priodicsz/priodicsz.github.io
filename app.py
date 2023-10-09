# app.py

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///support.db'
db = SQLAlchemy(app)

class SupportCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

@app.route('/')
def home():
    support_count = SupportCount.query.first()
    if not support_count:
        support_count = SupportCount()
        db.session.add(support_count)
        db.session.commit()
    return render_template('index.html', support_count=support_count.count)

@app.route('/increment_support', methods=['POST'])
def increment_support():
    support_count = SupportCount.query.first()
    if support_count:
        support_count.count += 1
        db.session.commit()
        return str(support_count.count)
    else:
        return '0'

@app.route('/get_support_count')
def get_support_count():
    support_count = SupportCount.query.first()
    if not support_count:
        return '0'
    return str(support_count.count)

if __name__ == '__main__':
    with app.app_context():  # Menambahkan konteks aplikasi Flask
        db.create_all()
    app.run(debug=True)