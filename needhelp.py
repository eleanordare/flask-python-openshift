from flask import Flask, request
from flask import render_template
from flask import redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flaskrun import flaskrun

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class NeedHelpEvent(db.Model):
	__tablename__ = 'needhelpevents'
	id = db.Column(db.Integer, primary_key=True)
	start_time = db.Column(db.Date)	
	end_time = db.Column(db.Date)
	
	def __init__(self, start_time, end_time):
		self.start_time = start_time
		self.end_time = end_time 

#    def __repr__(self):
#        return '<Content %s>' % self.content
db.drop_all()
db.create_all()

@app.route('/')
def need_help_events_list():
    events = NeedHelpEvent.query.all()
    return render_template('needhelpevents.html', needhelpevent=events)

@app.route('/needhelp', methods=['POST'])
def add_help_event():
    start_time = request.form['Start Time']
    end_time = request.form['End Time']
    if not start_time:
        return 'Error'

    if not end_time:
        return 'Error'

    fmt = "%Y-%m-%d"
    event = NeedHelpEvent(datetime.strptime(start_time, fmt), datetime.strptime(end_time, fmt))
    db.session.add(event)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    flaskrun(app)
