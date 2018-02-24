import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
import multiprocessing

def getPoetsPage(base_link):
	page = requests.get(base_link)
	html_doc = page.text
	soup = BeautifulSoup(html_doc, 'html.parser')

	poet_names = soup.find(class_ = 'approach')

	poet_names_list = poet_names.find_all('a')

	links = []
	for poets in poet_names_list:
		names = poets.contents[0]
		# print(poets.get('href'))
		links.append([poets.get('href'), poets.get('title')])
	return links

def getPoems_from_poets(base_link):
	page = requests.get(base_link)
	html_doc = page.text
	soup = BeautifulSoup(html_doc, 'html.parser')

	poem_names = soup.find(class_ = 'r')

	poem_list = []
	if poem_names == None:
		return poem_list
	
	for link in poem_names.find_all('h3'):
	    poem_list.append(link.find('a'))

	poem_links = []
	for poem in poem_list:
		# print(poem.get('href'))
		poem_links.append(poem.get('href'))

	return poem_links

def get_poem_from_page(base_link):
	page = requests.get(base_link)
	html_doc = page.text
	soup = BeautifulSoup(html_doc, 'html.parser')

	poem_names = soup.find(class_ = 'present')

	poem = "<start>\n"
	for para in poem_names.find_all('p'):
		print(para.get_text().strip())
		poem += para.get_text()
	poem += "<end>\n"
	return poem

########################## RUNNER ##################################

def processCrawl(link):
	poem_list = []
	for page_num in range(1, 10):
		# print(str(link[0][:-12]) + str(page_num) + ".sairbul.com")
		poem_list = getPoems_from_poets(str(link[0][:-12]) + str(page_num) + ".sairbul.com")
		if(poem_list == None):
			exit()
	for poem in poem_list:
		with open('Data2/'+ link[1] +'.txt', 'a') as the_file:
			the_file.write(get_poem_from_page(poem) + "\n")


def __main__():

	num_cores = multiprocessing.cpu_count()
	l = getPoetsPage("http://www.sairbul.com")

	Parallel(n_jobs=num_cores)(delayed(processCrawl)(i) for i in l)

__main__()