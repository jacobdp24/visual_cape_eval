from flask import Flask, render_template, flash, request, url_for, redirect, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
import sqlite3
import database as db
import sys


app = Flask(__name__)
app.config['SECRET_KEY'] = "super secret key" #change before production

class classForm(FlaskForm):
	findClass = StringField('findClass')

class searchForm(FlaskForm):

	professor = StringField('professor', description="test") #add the validator parameter
	classCode = StringField('classCode')

'''@app.route('/')
def mainPage():
	return render_template("main.html")'''

@app.route('/', methods=["GET", "POST"])
def searchpage():
	#you are at /list/ and that needs to be fixed
	try:
		
		form = searchForm(request.form)

		#and form.validate()

		if request.method == "POST":

			data = db.database('./data.db')


			#professor = request.form['professor']
			#classCode = request.form['classCode']
			#exClass = request.form['exClassCode']

			professor = request.form.get('professor')
			professor = request.form.get('classCode')
			exClass = request.form.get('exClassCode')

			teacherList = data.queryProfessorNames(exClass)

			if len(professorC) > 0:
				profData = data.querySpecificProfessor(professorC[0], professorC[1], classCode)

			professorC = data.cleanInputName(professor)

			profData = []

			#figure out logic to handle the forms here
			if not teacherList:
				#put in fail page for the main_list here
				return render_template('main_list.html', teacherList='nope')
			elif len(teacherList) > 0:
				return render_template('main_list.html', teacherList=teacherList)


			if len(profData) > 0:

				first = professorC[1]
				last = professorC[0]
				labels = data.queryTerm(professorC[0], professorC[1], classCode)
				recommendI = data.queryRecI(professorC[0], professorC[1], classCode)
				recommendC = data.queryRecC(professorC[0], professorC[1], classCode)
				studyHours = data.queryStudyHours(professorC[0], professorC[1], classCode)
				avgE = data.queryAvgExpected(professorC[0], professorC[1], classCode)
				avgR = data.queryAvgReceived(professorC[0], professorC[1], classCode)

				return render_template("display.html", professor=professor, classCode=classCode, first=first, last=last, labels=labels, recommendI=recommendI, recommendC=recommendC, studyHours=studyHours, avgR=avgR, avgE=avgE)

				#add in fail page


				#form is out
			return render_template("main.html")

			data.close()

			#logic for database queries will follow here

			#flash(classCode)
			#flash(professor)
		
		
		#form is out 
		return render_template('main.html')
	
	except Exception as e:
		flash(e)
		#form is out
		return render_template("main.html")
		
'''@app.route('/list/', methods=["GET","POST"])
def listClasses():

	form = classForm(request.POST)

	if request.method == "POST":

		exClass = request.form['exClassCode']

		print(exClass, file=sys.stdout)

		if exClass != None:

			return render_template('main_list.html', form=form, exClass=exClass)

		else:

			redirect(url_for('/'))'''


@app.route('/display/')
def display():

	return render_template("display.html")

if __name__ == "__main__":
	app.run(debug=True)