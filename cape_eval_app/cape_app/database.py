import sqlite3

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

	def create_table_professors(self):

		#self.c.execute('CREATE TABLE IF NOT EXISTS {}(course TEXT, term TEXT, enroll INTEGER, evals INTEGER, recommend_class REAL, recommend_instructor REAL, study_hours REAL, avg_expected TEXT, avg_received TEXT)'.format(prof))
		self.c.execute('CREATE TABLE IF NOT EXISTS professors (professor TEXT, course TEXT, term TEXT, enroll TEXT, evals TEXT, recommend_class TEXT, recommend_instructor TEXT, study_hours TEXT, avg_expected TEXT, avg_received TEXT)')
		self.commit()

	def create_table_subjectcode(self):

		self.c.execute("CREATE TABLE IF NOT EXISTS subjectcode(teacher TEXT PRIMARY KEY, subjectcode TEXT)")
		self.commit()


	def deleteTable(self, tableName):

		self.c.execute("DROP TABLE IF EXISTS %s" % (tableName))

	#TODO Methods
	
	def insert_teacher_subject(self, subject, prof):

		self.c.execute("INSERT OR IGNORE INTO subjectcode (teacher, subjectcode) VALUES (?, ?)",
			(prof, subject)) # "or ignore" prevents duplicates from being added
		self.commit() 

	
	def insert_teacher_data(self, ListOfTuplesToEnter):

		self.c.executemany("INSERT INTO professors VALUES (?,?,?,?,?,?,?,?,?,?)", ListOfTuplesToEnter) 
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
			print(data)
			dataList.append(data)

		return dataList

	'''
	query evals column from a professor  

	'''
	def queryEvals(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT evals FROM professors WHERE professor LIKE ?", tupleToQ):
			print(data)
			dataList.append(data)

		return dataList

	'''

	query course column for a professor

	'''

	def queryCourse(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT course FROM professors WHERE professor LIKE ?", tupleToQ):
			print(data)
			dataList.append(data)

		return dataList


	'''

	query term column for a professor 

	'''
	def queryTerm(self, professor):
		
		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT term FROM professors WHERE professor LIKE ?", tupleToQ):
			print(data)
			dataList.append(data)

		return dataList

	'''
	query enroll column for a professor 

	'''
	def queryEnroll(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT enroll FROM professors WHERE professor LIKE ?", tupleToQ):
			print(data)
			dataList.append(data)

		return dataList

	'''
	
	query percentage of recommended class for a professor

	'''
	def queryRecommendedClass(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT recommend_class FROM professors WHERE professor LIKE ?", tupleToQ):
			print(data)
			dataList.append(data)

		return dataList

	'''

	query percentage of recommended instructor for a professor 

	'''
	def queryRecommendInstructor(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT recommend_instructor FROM professors WHERE professor LIKE ?", tupleToQ):
			print(data)
			dataList.append(data)

		return dataList

	'''
	query study hours associated with a professor 

	'''
	def queryStudyHours(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT study_hours FROM professors WHERE professor LIKE ?", tupleToQ):
			print(data)
			dataList.append(data)

		return dataList

	'''
	
	query Avg expected grade from a professor 

	'''
	def queryAvgExpected(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT avg_expected FROM professors WHERE professor LIKE ?", tupleToQ):
			print(data)
			dataList.append(data)

		return dataList

	'''

	query avg grade received from a professor 

	'''

	def queryAvgReceived(self, professor):

		tupleToQ = (professor,)

		dataList = []

		for data in self.c.execute("SELECT avg_recieved FROM professors WHERE professor LIKE ?", tupleToQ):
			print(data)
			dataList.append(data)

		return dataList


