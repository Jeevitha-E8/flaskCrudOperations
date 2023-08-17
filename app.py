import os
from flask import Flask,redirect,render_template,request,url_for,flash
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
 
 
#Creating model table for our CRUD database
class Data(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
 
 
    def __init__(self, name, email, phone):
 
        self.name = name
        self.email = email
        self.phone = phone
 
#This is the index route where we are going to
#query on all our employee data
@app.before_first_request
def create_tables():
    db.create_all()
@app.route('/')
def Index():
    all_data = Data.query.all() 
    return render_template("index.html",employees=all_data)
  
#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
 
 
        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Employee Inserted Successfully")
 
        return redirect(url_for('Index'))
 
 
#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
 
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
 
        db.session.commit()
        flash("Employee Updated Successfully")
 
        return redirect(url_for('Index'))
 
 
 
 
#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
 
    return redirect(url_for('Index'))
 
 
 
 
 
 
if __name__ == "__main__":
    app.run(debug=True)