'''

script cleans the data in the database

'''

import database as db 

data = db.database('./data.db')

data.create_proper_labels()

professors = data.clean_query_prof()

for name in professors:

	#query all relevant data and store in the respective lists

	codeAndCourses = data.queryCourse(name)

	terms = data.queryTerm(name)

	enrolls = data.queryEnroll(name) #change type: int

	evals = data.queryEvals(name) #change type: int 

	rClasses = data.queryRecommendedClass(name) #change type: float 

	rInstructors = data.queryRecommendInstructor(name) #change type: float 

	studyHours = data.queryStudyHours(name) #change type: float

	aExps = data.queryAvgExpected(name)

	aRecs = data.queryAvgReceived(name)

	#this nest works becuase they are all the same size
	for j in range(len(evals)):

		#clean the codeAndCourse List first

		codeAndCourse = codeAndCourses[j]

		codeAndCourse = str(codeAndCourse[0])

		codeAndCourse = codeAndCourse.split(' ')

		code = codeAndCourse[0] + ' ' + codeAndCourse[1]

		code = (code,)

		#change type of enrolls

		enroll = enrolls[j]

		enroll = enroll[0]

		enroll = int(enroll)

		enroll = (enroll,)

		#change type of evals

		evalu = evals[j]

		evalu = evalu[0]

		evalu = int(evalu)

		evalu = (evalu,)

		#change type of rClass

		rClass = rClasses[j] 

		rClass = rClass[0]

		rClass = rClass.split(' ')

		rClass = rClass[0]

		rClass = float(rClass)

		rClass = (rClass,)

		#change type instructors 

		rInstructor = rInstructors[j]

		rInstructor = rInstructor[0]

		rInstructor = rInstructor.split(' ')

		rInstructor = rInstructor[0]

		rInstructor = float(rInstructor)

		rInstructor = (rInstructor,)		

		#change type study hours	

		studyHour = studyHours[j]

		studyHour = studyHour[0]

		studyHour = float(studyHour)

		studyHour = (studyHour,)

		#now create the tuple to insert and insert it

		tupleI = ()

		tupleI = (name,) + code + codeAndCourses[j] + terms[j] + enroll + evalu + rClass + rInstructor + studyHour + aExps[j] + aRecs[j]
		
		data.insert_clean(tupleI)

data.close()