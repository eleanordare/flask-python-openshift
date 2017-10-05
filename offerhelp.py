from flask import Flask, request
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flaskrun import flaskrun

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class OfferHelp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    what = db.Column(db.Text)
    when = db.Column(db.Text)

    def __init__(self, what, when):
        self.what = what
        self.when = when

    def __repr__(self):
        return '<Offer: %s | %s>' % self.what, self.when

db.create_all()

@app.route('/')
def offer_help():
    offers = OfferHelp.query.all()
    return render_template('offerHelp.html', offers=offers)

@app.route('/addhelp', methods=['POST'])
def addHelp():
   what = request.form['what']
   if not what:
       return "Error: We don't know what you wan't to do. Please share this with us!"
   when = request.form['when']
   if not when:
       return "We appreciate that you wan't to offer your time always. Still please submit a time where you wan't to help others with your valuable time!"

   offerhelp = OfferHelp(what, when)
   db.session.add(offerhelp)
   db.session.commit()

   return redirect('/')

if __name__ == '__main__':
    flaskrun(app)

