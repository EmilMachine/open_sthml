import urllib2
from bs4 import BeautifulSoup

### GET RAW XML
data_path = 'http://data.stockholm.se/set/Befolkning/Flyttningar/?apikey=S8O2CD27J2K4EE55CED0L0J5H81A1902'
page = urllib2.urlopen(data_path).read()

### PARSE XML
soup = BeautifulSoup(page,'lxml')

### xml specific / todo generalize
def soup2list(soup,key):
	tmp = [elem.string for elem in soup.findAll(key)]
	return tmp

area_code = soup2list(soup,'AREA_CODE')
year = soup2list(soup,'year')
moved_code = soup2list(soup, 'FLYTT3K_CODE')
moved = soup2list(soup, 'FLYTT6_ANTAL')

# TODO add type casting (to int etc)
# TODO convert to pandas obj
# TODO simple plot 



# Find fields in tag (http://stackoverflow.com/questions/10947968/xml-to-pandas-dataframe)
#DataFrame.from_records([(int(word['x1']), int(word['x2']))
#                        for word in soup.page.findAll('word')],
#                       columns=('x1', 'x2'))
