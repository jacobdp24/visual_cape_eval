import sqlite3
import re

class database:

	def __init__(self, path_to_database):

		#create database if it does not exist
		self.conn = sqlite3.connect(path_to_database)

		#connect to a cursor for the database
		self.c = self.conn.cursor()

		self.conn.row_factory = sqlite3.Row

	#always commit when using the database and then close when done       
	def commit(self):
		self.conn.commit()

	def close(self):
		self.conn.close()

	def getConnection(self):

		return self.c, self.conn

	'''
	create tables when originally scraping

	'''
	def create_table_professors(self):

		#self.c.execute('CREATE TABLE IF NOT EXISTS {}(course TEXT, term TEXT, enroll INTEGER, evals INTEGER, recommend_class REAL, recommend_instructor REAL, study_hours REAL, avg_expected TEXT, avg_received TEXT)'.format(prof))
		self.c.execute('CREATE TABLE IF NOT EXISTS professors (professor TEXT, course TEXT, term TEXT, enroll TEXT, evals TEXT, recommend_class TEXT, recommend_instructor TEXT, study_hours TEXT, avg_expected TEXT, avg_received TEXT)')
		self.commit()

	'''
	split up class by code and name
	and add the proper types to the inputs

	'''
	def create_proper_labels(self):

		self.c.execute('CREATE TABLE IF NOT EXISTS clean_professors (Last_Name TEXT, First_Name TEXT, Middle_Initial Text, course_code TEXT, course_name TEXT, term TEXT, enroll INTEGER, evals INTEGER, recommend_class REAL, recommend_instructor REAL, study_hours REAL, avg_expected TEXT, avg_received TEXT)')
		self.commit()

	'''
	get original subject codes to get the names of teachers

	'''
	def create_table_subjectcode(self):

		self.c.execute("CREATE TABLE IF NOT EXISTS subjectcode(teacher TEXT PRIMARY KEY, subjectcode TEXT)")
		self.commit()


	def deleteTable(self, tableName):

		self.c.execute("DROP TABLE IF EXISTS %s" % (tableName))

	
	'''
	insert into the subjectcode table 

	'''
	def insert_teacher_subject(self, subject, prof):

		self.c.execute("INSERT OR IGNORE INTO subjectcode (teacher, subjectcode) VALUES (?, ?)",
			(prof, subject)) # "or ignore" prevents duplicates from being added
		self.commit() 

	
	'''
	insert into the professors table
	'''
	def insert_teacher_data(self, ListOfTuplesToEnter):

		self.c.executemany("INSERT INTO professors VALUES (?,?,?,?,?,?,?,?,?,?)", ListOfTuplesToEnter) 
		self.commit()

	def insert_clean(self, tupleToEnter):

		self.c.execute("INSERT INTO clean_professors VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", tupleToEnter)
		self.commit()

	'''
	method returns a list of professor names from the database

	'''
	def query_professors(self):

		self.c.execute("SELECT * FROM subjectcode")
		r = self.c.fetchall()

		professors = []

		for name in r:

			prof = name[0]

			prof = [prof]

			professors = professors + prof


		return professors

	'''
	cleans the list before returned

	'''

	def clean_query_prof(self):

		self.c.execute("SELECT * FROM subjectcode")
		r = self.c.fetchall()

		professors = []

		i = 0

		for name in r:

			if i >= 1319 and i <= 1386:

				continue

			elif i >= 1867 and i <= 1908:

				continue

			elif i >= 2175 and i <= 2183:

				continue

			elif i >= 2236 and i <= 2250:

				continue

			elif i >= 3382 and i <= 3539:

				continue

			else:

				prof = name[0]

				prof = [prof]

				professors = professors + prof

			i += 1

		return professors


	# the following query methods will be used to clean data, more query methods will
	# be needed to obtain the results for a specific class

	'''
	query all data associated with a professor

	'''
	def queryAll(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT * FROM professors WHERE professor LIKE ?", tupleToQ):
			
			dataList.append(data)

		return dataList


	'''
	query evals column from a professor  

	'''
	def queryEvals(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT evals FROM professors WHERE professor LIKE ?", tupleToQ):
			
			dataList.append(data)

		return dataList

	'''

	query course column for a professor

	'''

	def queryCourse(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT course FROM professors WHERE professor LIKE ?", tupleToQ):
		
			dataList.append(data)

		return dataList


	'''

	query term column for a professor 

	'''
	def queryTerm(self, professor):
		
		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT term FROM professors WHERE professor LIKE ?", tupleToQ):
			
			dataList.append(data)

		return dataList

	'''
	query enroll column for a professor 

	'''
	def queryEnroll(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT enroll FROM professors WHERE professor LIKE ?", tupleToQ):
			
			dataList.append(data)

		return dataList

	'''
	
	query percentage of recommended class for a professor

	'''
	def queryRecommendedClass(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT recommend_class FROM professors WHERE professor LIKE ?", tupleToQ):
			dataList.append(data)

		return dataList

	'''

	query percentage of recommended instructor for a professor 

	'''
	def queryRecommendInstructor(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT recommend_instructor FROM professors WHERE professor LIKE ?", tupleToQ):
			
			dataList.append(data)

		return dataList

	'''
	query study hours associated with a professor 

	'''
	def queryStudyHours(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT study_hours FROM professors WHERE professor LIKE ?", tupleToQ):
			
			dataList.append(data)

		return dataList

	'''
	
	query Avg expected grade from a professor 

	'''
	def queryAvgExpected(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT avg_expected FROM professors WHERE professor LIKE ?", tupleToQ):
			
			dataList.append(data)

		return dataList

	'''

	query avg grade received from a professor 

	'''

	def queryAvgReceived(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT avg_received FROM professors WHERE professor LIKE ?", tupleToQ):
			
			dataList.append(data)

		return dataList

	'''
	The following query methods will pull data from the
	properly formatted table and will need the class code
	and professor first name, last name, or middle initial

	'''

	'''
	this method has the precondition that the user supplied a complete professor 
	name with the correct class code, this is the best case 

	@return - a list of tuples containing the data corresponding the the class and professor
	'''
	def querySpecificProfessor(self, last, first, middle, code):

		tupleToQ = (last, first, middle, code)

		dataList = []

		# TODO: MAKE THESE QUERIES CASE INSENSITIVE

		for data in self.c.execute("SELECT * FROM clean_professors WHERE Last_Name=? AND First_Name=? AND Middle_Initial=? AND course_code=?", tupleToQ):

			dataList.append(data)

		return dataList


	'''
	this method has the precondition that the user supplied a complete professor 
	name with the correct class code, this is the best case but without the middle name
	need to handle the edge case of multiples of the same class taught during one quarter

	@return - a list of tuples containing the data corresponding the the class and professor
	'''
	def querySpecificProfessor(self, last, first, code):

		tupleToQ = (last, first, code)

		dataList = []

		for data in self.c.execute("SELECT * FROM clean_professors WHERE First_Name=? COLLATE NOCASE AND Last_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):

			dataList.append(data)

		if len(dataList) == 0:
			for data in self.c.execute("SELECT * FROM clean_professors WHERE Last_Name=? COLLATE NOCASE AND First_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):

				dataList.append(data)

		return dataList


	def queryEvals(self, last, first, code):
		
		tupleToQ = (last, first, code)

		tupleList = []

		for data in self.c.execute("SELECT evals FROM clean_professors WHERE First_Name=? COLLATE NOCASE AND Last_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
			
			tupleList.append(data)

		if len(tupleList) == 0:
			
			for data in self.c.execute("SELECT evals FROM clean_professors WHERE Last_Name=? COLLATE NOCASE AND First_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
			
				tupleList.append(data)

		dataList = []

		for tuples in reversed(tupleList):

			dataList.append(tuples[0])

		return dataList

	def queryEnrolls(self, last, first, code):
		
		tupleToQ = (last, first, code)

		tupleList = []
		
		for data in self.c.execute("SELECT enroll FROM clean_professors WHERE First_Name=? COLLATE NOCASE AND Last_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
			
			tupleList.append(data)


		if len(tupleList) == 0:

			for data in self.c.execute("SELECT enroll FROM clean_professors WHERE Last_Name=? COLLATE NOCASE AND First_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
			
				tupleList.append(data)

		dataList = []

		for tuples in reversed(tupleList):

			dataList.append(tuples[0])

		return dataList

	'''

	query term column for a professor from cleaned input

	'''
	def queryTerm(self, last, first, code):
		
		tupleToQ = (last, first, code)

		tupleList = []

		for data in self.c.execute("SELECT term FROM clean_professors WHERE First_Name=? COLLATE NOCASE AND Last_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
				
				tupleList.append(data)

		if len(tupleList) == 0:
			
			for data in self.c.execute("SELECT term FROM clean_professors WHERE Last_Name=? COLLATE NOCASE AND First_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
				
				tupleList.append(data)

		dataList = []

		for tuples in reversed(tupleList):

			dataList.append(tuples[0])

		return dataList

	def queryRecI(self, last, first, code):
		
		tupleToQ = (last, first, code)

		tupleList = []

		for data in self.c.execute("SELECT recommend_instructor FROM clean_professors WHERE First_Name=? COLLATE NOCASE AND Last_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
				
			tupleList.append(data)

		if len(tupleList) == 0:

			for data in self.c.execute("SELECT recommend_instructor FROM clean_professors WHERE Last_Name=? COLLATE NOCASE AND First_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
				
				tupleList.append(data)

		dataList = []

		for tuples in reversed(tupleList):

			dataList.append(tuples[0])

		return dataList

	def queryRecC(self, last, first, code):
		
		tupleToQ = (last, first, code)

		tupleList = []

		for data in self.c.execute("SELECT recommend_class FROM clean_professors WHERE First_Name=? COLLATE NOCASE AND Last_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
				
			tupleList.append(data)


		if len(tupleList) == 0:

			for data in self.c.execute("SELECT recommend_class FROM clean_professors WHERE Last_Name=? COLLATE NOCASE AND First_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
				
				tupleList.append(data)

		dataList = []

		for tuples in reversed(tupleList):

			dataList.append(tuples[0])

		return dataList

	def queryAvgReceived(self, last, first, code):
		
		tupleToQ = (last, first, code)

		tupleList = []

		for data in self.c.execute("SELECT avg_received FROM clean_professors WHERE First_Name=? COLLATE NOCASE AND Last_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
				
			tupleList.append(data)

		if tupleList == 0:

			for data in self.c.execute("SELECT avg_received FROM clean_professors WHERE Last_Name=? COLLATE NOCASE AND First_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
				
				tupleList.append(data)

		dataList = []

		for tuples in reversed(tupleList):

			dataList.append(tuples[0])

		gpa = []
		letterList = []

		for string in dataList:

			firstSplit = string.split(' ')
			letterList.append(firstSplit[0])

			if len(firstSplit) > 1:
				secondSplit = firstSplit[1].split('(')
				thirdSplit = secondSplit[1].split(')')
				gpa.append(float(thirdSplit[0]))

			else:
				gpa.append(0)
		
		return gpa

	def queryAvgExpected(self, last, first, code):
		
		tupleToQ = (last, first, code)

		tupleList = []

		for data in self.c.execute("SELECT avg_expected FROM clean_professors WHERE First_Name=? COLLATE NOCASE AND Last_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):

			tupleList.append(data)

		if len(tupleList) == 0:
			
			for data in self.c.execute("SELECT avg_expected FROM clean_professors WHERE Last_Name=? COLLATE NOCASE AND First_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):

				tupleList.append(data)

		dataList = []

		for tuples in reversed(tupleList):

			dataList.append(tuples[0])

		gpa = []
		letterList = []

		for string in dataList:

			firstSplit = string.split(' ')
			letterList.append(firstSplit[0])

			if len(firstSplit) > 1:
				secondSplit = firstSplit[1].split('(')
				thirdSplit = secondSplit[1].split(')')
				gpa.append(float(thirdSplit[0]))

			else:
				gpa.append(0)
		
		return gpa

	def queryStudyHours(self, last, first, code):
		
		tupleToQ = (last, first, code)

		tupleList = []

		for data in self.c.execute("SELECT study_hours FROM clean_professors WHERE First_Name=? COLLATE NOCASE AND Last_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
				
			tupleList.append(data)

		if len(tupleList) == 0:

			for data in self.c.execute("SELECT study_hours FROM clean_professors WHERE Last_Name=? COLLATE NOCASE AND First_Name=? COLLATE NOCASE AND course_code=?", tupleToQ):
				
				tupleList.append(data)

		dataList = []

		for tuples in reversed(tupleList):

			dataList.append(tuples[0])

		return dataList
	
	def queryProfessorNames(self, classCode):

		acceptableCourses = []

		for course in self.c.execute("SELECT course_code FROM clean_professors"):
			course = course[0]
			acceptableCourses.append(course)

		if classCode not in acceptableCourses:

			return False

		else:
			tupleToQ = (classCode,)

			lastNames = []
			firstNames = []
			fullNames = []

			for lastName in self.c.execute("SELECT Last_Name FROM clean_professors WHERE course_code LIKE ?", tupleToQ):
				lastNames.append(lastName)

			for firstName in self.c.execute("SELECT First_Name FROM clean_professors WHERE course_code LIKE ?", tupleToQ):
				firstNames.append(firstName)
			
			for i in range(len(firstNames)):
				lastName = lastNames[i]
				lastName = lastName[0]
				firstName = firstNames[i]
				firstName = firstName[0]

				combined = lastName + ', ' + firstName

				if combined not in fullNames:
					fullNames.append(combined)

			return fullNames

	def nameAgnostic(self, first, last, classCode):

		labels = self.queryTerm(first, last, classCode)
		recommendI = self.queryRecI(first, last, classCode)
		recommendC = self.queryRecC(first, last, classCode)
		studyHours = self.queryStudyHours(first, last, classCode)
		avgE = self.queryAvgExpected(first, last, classCode)
		avgR = self.queryAvgReceived(first, last, classCode)
		enrolls = self.queryEnrolls(first, last, classCode)
		evals = self.queryEvals(first, last, classCode)

		dictToReturn = {'labels': labels,
						'recommendI': recommendI,
						'recommendC': recommendC,
						'studyHours': studyHours,
						'avgE': avgE,
						'avgR': avgR,
						'enrolls': enrolls,
						'evals': evals
						}


		return dictToReturn
		
		

		#first check first and last name (most likely)
			#set boolean
		#then check last and first name (second most likely)
			#set boolean
		
		#if first
			#build dic
		#elif second
			#build dic
		#else
			#return blank as normal

	def queryProfsAutoComplete(self):

		lastNames = []
		firstNames = []
		fullNames = []
		listReturn = []

		for lastName in self.c.execute("SELECT Last_Name FROM clean_professors"):
			lastNames.append(lastName)

		for firstName in self.c.execute("SELECT First_Name FROM clean_professors"):
			firstNames.append(firstName)
			
		for i in range(len(firstNames)):
			lastName = lastNames[i]
			lastName = lastName[0]
			firstName = firstNames[i]
			firstName = firstName[0]

			combined = lastName + ', ' + firstName

			if combined not in fullNames:
				fullNames.append(combined)
				name = {'name': combined}
				listReturn.append(name)

		return listReturn

	def queryClassAutoComplete(self):

		courseCodes = []
		listReturn = []

		for code in self.c.execute("SELECT course_code FROM clean_professors"):
			if code[0] not in courseCodes:
				courseCodes.append(code[0])
				codeDict = {'code': code[0]}
				listReturn.append(codeDict)

		return listReturn

	#TODO finish the query cases for edge case inputs (found professor but not class or vice versa)

	'''
	the following methods validate if an input exists in the database

	'''

	'''
	cleans an input name so its just the first and last names
	'''
	def cleanInputName(self, professor):

		#TODO edge case of apostrophes of hyphens in names 
		stringS = re.compile(r'[a-zA-Z]*')

		mo = stringS.findall(professor)

		mo = [x for x in mo if x != '']

		print(len(mo))

		return mo

if __name__=="__main__":
	data = database('./data.db')
	
	print(data.queryProfsAutoComplete())
	data.close()




		

		





