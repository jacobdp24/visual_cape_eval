from flask import Flask, render_template, flash, request, url_for, redirect
import sqlite3
import database as db
import sys

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

			data = db.database('./data.db')

			professorC = data.cleanInputName(professor)

			profData = data.querySpecificProfessor(professorC[0], professorC[1], classCode)

			if len(profData) > 0:

				labels = data.queryTerm(professorC[0], professorC[1], classCode)
				recommendI = data.queryRecI(professorC[0], professorC[1], classCode)
				recommendC = data.queryRecC(professorC[0], professorC[1], classCode)


				return render_template("display.html", professor=professor, classCode=classCode, labels=labels, recommendI=recommendI, recommendC=recommendC)

			else:

				return render_template("display.html", professor="fail", classCode=classCode)

			data.close()

			#logic for database queries will follow here

			flash(classCode)
			flash(professor)
			
			#return redirect(url_for('display'))
			return render_template("display.html", professor=professor, classCode=classCode)
		
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