import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
import multiprocessing

def getPoetsPage(base_link):
	page = requests.get(base_link)
	html_doc = page.text
	soup = BeautifulSoup(html_doc, 'html.parser')

	useless_link = soup.find(class_='subject-list-title')
	useless_link.decompose()

	for div in soup.find_all("div", {'class':'poem-img'}):
	    div.decompose()

	poet_names = soup.find(class_ = 'popular-poem box list')

	poet_names_list = poet_names.find_all('a')

	links = []
	odd = False
	for poets in poet_names_list:
		names = poets.contents[0]
		if(odd):
			odd = False
			links.append('https://www.antoloji.com' + poets.get('href'))
		else:
			odd = True
	if str.isdigit(base_link[-3:-1]):
		print ("here ", base_link[-3:-1])
		return links, base_link[-3:-1]
	else:
		print (base_link[-2])
		return links, base_link[-2]

###########################SecondPage###########################

def getTheLinks(base_link, main_page_num):
	if main_page_num == 1:
		page = requests.get(base_link)
	else:
		page = requests.get(base_link + "ara-/sirala-/sayfa-" + str(main_page_num) + "/")
	html_doc = page.text
	soup = BeautifulSoup(html_doc, 'html.parser')

	links_of_poems = []
	for div in soup.find_all("div", {'class':'list-number'}):
		links_of_poems.append("https://www.antoloji.com" + div.find('a').get('href'))
		# print("https://www.antoloji.com" + div.find('a').get('href'))
		print("." , end="")
	return links_of_poems

############################ThirdPage#############################

def getThePoem(base_link, pageId):
	page = requests.get(base_link)
	html_doc = page.text
	soup = BeautifulSoup(html_doc, 'html.parser')

	poem = "<start>\n"
	for div in soup.find_all("div", {'class':'pd-text'}):
		for para in div.find_all('p'):
			# print(para.get_text().strip())
			properString = correctTheString(para.get_text())
			poem += properString

	poem += "<end>\n"
	with open('Data/siirler_page'+ str(pageId) +'.txt', 'a') as the_file:
		the_file.write(poem + "\n")

########################## RUNNER ##################################

def correctTheString(s):
	if (len(s.strip()) < 3):
		return ""
	else:
		return s.strip() + "\n"

def processCrawl(page_link):
	links, page_id = getPoetsPage(page_link)
	for link_of_poet in links:
		for i in range(7, 10):
			poem_links = getTheLinks(link_of_poet, i)
			for link in poem_links:
				getThePoem(link, page_id)

def __main__():

	# upper bound for pages is 18
	start_page = int(input("Start From Page number : "))
	how_many_pages = int(input("Crawl this many pages : "))
	# poems_page_count = int(input("How many pages do you want to crawl from each poet : "))
	pages = [] #['https://www.antoloji.com/populer-sairler/']
	for i in range(start_page, start_page + how_many_pages):
		pages.append("https://www.antoloji.com/populer-sairler/sirala-/sayfa-" + str(i) + "/")

	num_cores = multiprocessing.cpu_count()

	Parallel(n_jobs=num_cores)(delayed(processCrawl)(i) for i in pages)

__main__()