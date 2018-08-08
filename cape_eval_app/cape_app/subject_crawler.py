'''

Script populates the subjectcodes database for fast access to every
single professor name at UCSD.

'''

import database as db 
import scraper as s
import bs4
import requests
import time 

def main():

	data = db.database('./data.db')

	data.deleteTable('subjectcode')

	data.create_table_subjectcode()

	#driver = d.driver()
	scraper = s.scraper()

	blankSubjects = []

	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    	}

	print('# of subjects: ' + str(len(scraper.subjects)))

	begin = time.clock()

	for index in range(len(scraper.subjects)): #get the teachers based off of the subject codes

		url = 'http://www.cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber='

		subject = scraper.subjects[index]

		url = url + subject

		try:

			res = requests.get(url, headers=headers)

			#check for erros 
			res.raise_for_status()

		except Exception as e: 

			print(e)

		#parse the html 
		html = bs4.BeautifulSoup(res.text, 'html.parser')

		table = html.tbody #grab tbody tag

		circleIndex = 0 # help with only getting names

		#populate the subjectcode table for easy access to every teacher name

		if table is None:

			emptyTable = (index, subject)
			blankSubjects.append(emptyTable)

			continue

		else:

			for string in table.stripped_strings:

				if circleIndex % 10 == 0:

					data.insert_teacher_subject(subject, string)				

				circleIndex += 1

				#print(repr(string))

	end = time.clock()

	speed = end - begin

	print("time to load data: " + str(speed))

	print(blankSubjects)

	data.close()

if __name__ == "__main__":
	main()

