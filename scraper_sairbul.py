import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
import multiprocessing
import re

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
		unicode_string = poets.get('title').encode('latin1').decode('utf8')
		links.append([poets.get('href'), unicode_string])
	return links

def getPoems_from_poets(base_link):
	page = requests.get(base_link)
	html_doc = page.text
	soup = BeautifulSoup(html_doc, 'html.parser')

	poem_names = soup.find(class_ = 'r')
	if poem_names == None:
		return []

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
	if poem_names == None:
		print("Error parsing no class found: " + base_link)
		return ""

	poem = _with_tag_p(poem_names)
	if poem == "<start>\n":
		poem = _with_class(poem_names)
		if poem == "<start>\n":
			poem = _with_tag_span(poem_names)
			if poem == "<start>\n":
				print("Error parsing no paragraph link found: " + base_link)
				return ""
	poem += "\n<end>\n"
	# print(poem)
	return poem

def _with_class(poem_names):
	poem = "<start>\n"
	for para in poem_names.find_all(class_ = 'p pt5'):
		poem += (para.get_text("\n").encode('latin1', 'ignore').decode('utf8', "ignore"))
	return poem
def _with_tag_p(poem_names):
	poem = "<start>\n"
	for para in poem_names.find_all('p'):
		poem += (para.get_text("\n").encode('latin1', 'ignore').decode('utf8', "ignore"))
	return poem
def _with_tag_span(poem_names):
	poem = "<start>\n"
	for para in poem_names.find_all('span'):
		poem += (para.get_text("\n").encode('latin1', 'ignore').decode('utf8', "ignore"))
	return poem

########################## RUNNER ##################################

def processCrawl(link):
	poem_list = []
	for page_num in range(1, 10):
		poem_list += getPoems_from_poets(str(link[0][:-12]) + str(page_num) + ".sairbul.com")
		# if len() > 0:
		# 	print(str(link[0][:-12]) + str(page_num) + ".sairbul.com")

	for poem in poem_list:
		with open('Data2/'+ link[1] +'.txt', 'a') as the_file:
			the_file.write(get_poem_from_page(poem) + "\n")


def __main__():

	num_cores = multiprocessing.cpu_count()
	l = getPoetsPage("http://www.sairbul.com")
	# l = ['http://abdurrahim-karakoc.sairbul.com/acaba/', 'http://ahmet-hasim.sairbul.com/bir-yaz-gecesi-hatirasi/', 'http://ahmet-hasim.sairbul.com/agac/']
	Parallel(n_jobs=num_cores)(delayed(processCrawl)(i) for i in l[42:])

	# print(get_poem_from_page("http://ahmet-hasim.sairbul.com/agac/"))

__main__()