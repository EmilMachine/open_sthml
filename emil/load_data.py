import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

### GET RAW XML
data_path = 'http://data.stockholm.se/set/Befolkning/Flyttningar/?apikey=S8O2CD27J2K4EE55CED0L0J5H81A1902'
page = urllib2.urlopen(data_path).read()

### PARSE XML
soup = BeautifulSoup(page,'lxml')

### Extract list (usefull if assume table structure)
def soup2list(soup,key,method=str):
	tmp = [method(elem.string) for elem in soup.findAll(key)]
	return tmp

### xml specific / todo generalize?
# BYHAND
area_code = soup2list(soup,'area_code')
year = soup2list(soup,'year',int)
gender_code = soup2list(soup,'konk_code')
moved_code = soup2list(soup, 'flytt3k_code',int)
moved = soup2list(soup, 'flytt6_antal',int)
### TODO: FIX UNICODE ERROR
#area_text = soup2list(soup,'area_text')
#moved_text = soup2list(soup, 'flytt3k_text')
#gender = soup2list(soup,'konk_text')

### convert to pandas obj
# BYHAND
df = pd.DataFrame.from_records(
	zip(area_code,year,gender_code,moved_code,moved)
	, columns = ['area_code','year','gender_code','moved_code','moved']
	)


### simple plot 
# 1. aggregate
df2 = df[['year','gender_code','moved']].groupby(['year','gender_code']).sum()

# 2. plot
# See http://stackoverflow.com/questions/28293028/plotting-grouped-data-in-same-plot-using-pandas
fig, ax = plt.subplots(figsize=(8,6))

# See http://stackoverflow.com/questions/25386870/pandas-plotting-with-multi-index
df2.unstack(level=0).plot(kind='bar',ax=ax)
plt.ylabel('people moved')

plt.show()


# Find fields in tag (http://stackoverflow.com/questions/10947968/xml-to-pandas-dataframe)
#DataFrame.from_records([(int(word['x1']), int(word['x2']))
#                        for word in soup.page.findAll('word')],
#                       columns=('x1', 'x2'))
