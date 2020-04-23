from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import csv 

def get_disc(disc_p):
	Discour = ""
	for element in disc_p:
		Discour = Discour + element.text + "\n"
	return Discour	

def get_date(element):
	return element.find("span",{"class":"date-display-single"}).text

def get_title(disc):
	return disc.span.h2.a.text

def get_bs_page(url):	
	Cl = uReq(url)
	page = Cl.read()
	Cl.close()
	return bs(page, "html.parser")

def write_row_to_csv(row):
	with open("My_Data.csv" , 'a', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(row)


with open("My_Data.csv" , 'w', newline='') as f:
			writer = csv.DictWriter(f, fieldnames=["Title", "Discour", "Date"])
			writer.writeheader()



for year in range(2019,1998,-1): 
		page = 0
		my_url = "http://www.maroc.ma/fr/discours-du-roi?field_type_discours_royal_value_i18n=1&date_discours%5Bvalue%5D%5Byear%5D="

		my_url = my_url+str(year)
		i = 0
		while(True):

			bs0 = get_bs_page(my_url)
			try :
				discours = bs0.findAll("div",{"class":"discours"})[0]
			except IndexError:
				break

			page += 1 

			discours_p = discours.ul.findAll("li")
			Data = []

			for element in discours_p:

					Title = get_title(element)

					Ref = "http://www.maroc.ma"+element.span.h2.a["href"]

					bs_FTP = get_bs_page(Ref)

					Discour_p = bs_FTP.findAll("p")

					Date = get_date(element)

					Discour = get_disc(Discour_p)

					Data = ["*****"+Title, Discour, Date]

					write_row_to_csv(Data)

			my_url = my_url+"&page="+str(page)	

		
print("********************* DONE ********************")

