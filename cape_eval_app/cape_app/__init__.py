from flask import Flask, render_template, flash, request, url_for, redirect
import sqlite3
import sys
from secret import install_secret_key

app = Flask(__name__)
app.secret_key = "super secret key" #change before production

@app.route('/')
def mainPage():
	return render_template("main.html")

@app.route('/', methods=["GET","POST"])
def searchpage():

	try:
		
		if request.method == "POST":

			professor = request.form['professor']
			classCode = request.form['classCode']


			flash(classCode)
			flash(professor)


			#TODO make JSON serializable and check inputs
			'''
			if request.form['submit'] is 'search':
				professor = request.form['professor']
				classCode = request.form['classCode']
					
				#split the post for the professor 
				professor = professor.split('%2C+')

				professor = professor[0] + ', ' + professor[1]

				#split the post for the class code

				classCode = classCode.split('+')

				classCode = classCode[0] + ' ' + classCode[1]

				#flash(professor)
				#flash(classCode)

				
				
				conn = sqlite3.connect('data.db')
				c = conn.cursor()
				c.execute()
				

					#this is where I would check if professor and classCode match
					#anything is the db

					#just a test right now
					#if professor is 'philip' and classCode is 'CSE 12':

				#return redirect(url_for('display'))
			'''
			
			return redirect(url_for('display'))
		else:
		
			return redirect('/')
	
	except Exception as e:
		flash(e)
		print(str(e))
		return render_template("main.html")

	

@app.route('/display/')
def display():

	return render_template("display.html")

if __name__ == "__main__":
	app.run(debug=True)