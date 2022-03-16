from flask import Flask, render_template, url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)



class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_name = db.Column(db.String(20), nullable=False)
    link = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    
    def __repr__(self):
        return '<Link %r>' % self.id

@app.route('/', methods=['POST', "GET"])
def index():
    if request.method == "POST": # we can check if the request.form exist, if not, then skip
        if request.form['link']:
            link_name = request.form['link_name']
            link = request.form['link']
            new_link = Profile(link_name=link_name, link=link)
            try:
                db.session.add(new_link)
                db.session.commit()
                return redirect('/')
            except:
                return "There was an issue adding your link!"

    else:
        links = Profile.query.order_by(Profile.date_created).all()
        return render_template('index.html', links=links)


if __name__ == "__main__":
    app.run(debug=True)