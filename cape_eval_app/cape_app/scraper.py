import bs4
import requests


class scraper:

	def __init__(self):

		self.departments = []
		self.subjects = []

		#make sure website does't think I'm a bot
		headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    	}

    	#get the site 
		res = requests.get('http://www.cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=CSE', headers=headers)

		#check for erros 
		res.raise_for_status()

		#parse the html 
		html = bs4.BeautifulSoup(res.text, 'html.parser')

		pre_list = html.find_all('option')

		for department in pre_list:
			unabbreviated = department.text.strip()
			abbreviation = ''

			for character in unabbreviated:
				
				if (character.isspace()):

					break

				abbreviation += character

			self.departments.append(abbreviation)


		del self.departments[0]

		res = requests.get('https://blink.ucsd.edu/instructors/courses/schedule-of-classes/subject-codes.html', headers=headers)

		#check for erros 
		res.raise_for_status()

		html = bs4.BeautifulSoup(res.text, 'html.parser')

		dirty_list = html.find_all('td')

		for even in range(0, len(dirty_list)):

			if even % 2 is 0:
				elem2add = dirty_list[even]
				self.subjects.append(elem2add.text.strip())

		#print(self.subjects)




