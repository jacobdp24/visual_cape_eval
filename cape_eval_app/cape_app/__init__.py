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
		
		#form = searchForm(request.form)

		#and form.validate()

		if request.method == "POST":

			data = db.database('./data.db')


			#professor = request.form['professor']
			#classCode = request.form['classCode']
			#exClass = request.form['exClassCode']

			professor = request.form.get('professor')
			classCode = request.form.get('classCode')
			exClass = request.form.get('exClassCode')

			classCode = str(classCode)
			exClass = str(exClass)


			classCode = classCode.upper()
			exClass = exClass.upper()

			teacherList = data.queryProfessorNames(exClass)

			professorC = data.cleanInputName(professor)

			profData = None

			if len(professorC) > 0:

				name1 = professorC[0]
				name2 = professorC[1]

				name1 = name1.lower()
				name2 = name2.lower()

				profData = data.querySpecificProfessor(name1, name2, classCode)
			

			if len(profData) > 0:

				first = professorC[1]
				last = professorC[0]
				combine = first + ' ' + last

				labels = data.queryTerm(professorC[0], professorC[1], classCode)
				recommendI = data.queryRecI(professorC[0], professorC[1], classCode)
				recommendC = data.queryRecC(professorC[0], professorC[1], classCode)
				studyHours = data.queryStudyHours(professorC[0], professorC[1], classCode)
				avgE = data.queryAvgExpected(professorC[0], professorC[1], classCode)
				avgR = data.queryAvgReceived(professorC[0], professorC[1], classCode)
				enrolls = data.queryEnrolls(professorC[0], professorC[1], classCode)
				evals = data.queryEvals(professorC[0], professorC[1], classCode)


				return render_template("display.html", professor=combine, classCode=classCode, first=first, last=last, labels=labels, recommendI=recommendI, recommendC=recommendC, studyHours=studyHours, avgR=avgR, avgE=avgE, enrolls=enrolls, evals=evals)
				#return render_template('main_list.html', teacherList=first + ' ' + last)

				#add in fail page


			#figure out logic to handle the forms here
			if not teacherList and profData != None:
				#put in fail page for the main_list here
				return render_template('main_list.html', teacherList='professor or class not found')
			elif len(teacherList) > 0:
				return render_template('main_list.html', teacherList=teacherList, exClass = exClass)
			

			

				#form is out
			return render_template("main.html")

			data.close()

			#flash(classCode)
			#flash(professor)
		
		
		#form is out 
		return render_template('main.html')
	
	
	#except AttributeError:
	#	return render_template('main_list.html', teacherList=classCode)


	except IndexError:
		return render_template('main_list.html', teacherList='when do I get Index errors')

	except TypeError:
		if not teacherList:
			return render_template('main_list.html', teacherList='class not found in lower search bar')

		else:
			return render_template('main_list.html', teacherList=teacherList)

	except Exception as e:
		flash(e)
		#form is out
		return render_template("main.html")
		


@app.route('/display/')
def display():

	return render_template("display.html")

if __name__ == "__main__":
	app.run(debug=True)