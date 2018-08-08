'''

script populates individual tables for each professor,
containing the data that the cape eval website has

'''

import database as db 
import scraper as s
import bs4
import requests
import time

def main():
	
	#connect 
	data = db.database('./data.db')

	#get list 
	profs = data.clean_query_prof()

	data.create_table_professors()

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}

	begin = time.clock()

	loading = 1 

	length = len(profs)

	#iterate professors 
	for name in profs:

		print("starting " + name + " " + str(loading) + "/" + str(length))

		addition = '+'

		lastFirst = name.split(',')

		newLast = lastFirst[0] + '%2C'

		newFirst = lastFirst[1].split(' ')

		newFirst = addition.join(newFirst)

		lastFirst = newLast + newFirst

		#create the URL specific for the professor
		url = 'http://www.cape.ucsd.edu/responses/Results.aspx?Name=%s&CourseNumber=' % (lastFirst)

		
		try:

			res = requests.get(url, headers=headers)

			#check for erros 
			res.raise_for_status()

		except Exception as e: 

			print(e)

		#parse the html 
		html = bs4.BeautifulSoup(res.text, 'html.parser')

		table = html.tbody #grab tbody tag

		#list to store data for the professor 
		profData = []

		tupleToInsert = ()

		print("inputting data for " + name)

		#iterate through the strings
		for string in table.stripped_strings:

			#once a row has been added 
			if len(tupleToInsert) == 10:

				#append to the list that will be inserted 
				profData.append(tupleToInsert)

				#clear the tuple
				tupleToInsert = ()		

			#append the data to the tuple 
			tupleToInsert = tupleToInsert + (string,)


		print(profData)
		data.insert_teacher_data(profData) #insert professor specific data 
		print(name + ' data has been inserted. ' +  str((loading/length) * 100) + '%')
		loading += 1

	end = time.clock()

	speed = end - begin

	print("time to load data: " + str(speed))

	#close connection
	data.close()

if __name__ == "__main__":

	main()
