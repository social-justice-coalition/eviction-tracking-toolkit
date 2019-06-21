
# coding: utf-8

# In[1]:


# import libraries
import requests
from bs4 import BeautifulSoup
import urllib
import re
import pandas as pd


# In[2]:


import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()


# In[3]:


import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


# In[177]:


MyEmptydf = pd.DataFrame()


# In[4]:


#this function is for getting content of the case
def url_to_string(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html5lib')
    for script in soup(["script", "style", 'aside']):
        script.extract()
    return " ".join(re.split(r'[\n\t]+', soup.get_text()))


# In[663]:


yearinput = input("Enter a year: ")


# In[664]:


quote_page = "http://saflii.org/za/cases/ZAWCHC/" + yearinput + "/"


# In[665]:


# query the website and return the html to the variable ‘page’
page = requests.get(quote_page)
# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page.content, 'html.parser')
# Take out the <div> of name and get its value
all_a=soup.find('td').find_all('a', attrs={'class': 'make-database'})


# In[666]:


all_url=[]
for a in all_a:
    url="http://saflii.org/za/cases/ZAWCHC"+ a['href'][2:]
    all_url.append(url)


# In[667]:


occupierurl=[]


# In[668]:


for url in all_url:
    page=url_to_string(url)
    if 'Prevention of Illegal Eviction' in page:
        print(url , "has PIE")
        occupierurl.append(url)
if occupierurl == []:
        print('no case about PIE')


# In[669]:


mylist = list(set(occupierurl))


# In[670]:


data = {'url':mylist}


# In[671]:


df = pd.DataFrame(data)


# In[672]:


casenumber = []


# In[673]:


#casenumber = []
for url in df['url']:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title=soup.find('div', attrs={'id': 'squeeze'}).find('h2').get_text()
    title=title.replace('\n    ', '')
    title=title.replace('\n  ', '')
    #print(title)
    casenumber.append(title)
    #print("new for",url)
#casenumber  


# In[674]:


df['title']=casenumber


# In[675]:


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


# In[676]:


caseno=[]
judgmentdate=[]


# In[677]:


for s in casenumber:
    var = re.findall('\((.*?)\)',s)
    judgmentdate.append(var[-1])
    var.pop(-1)


# In[678]:


df['judgment date']=judgmentdate


# In[679]:


for s in casenumber:
    var = re.findall('\((.*?)\)',s)
    judgmentdate.append(var[-1])
    var.pop(-1)
    for item in var:
        if hasNumbers(item) == True and len(item) > 3:
            caseno.append(item)
            break;


# In[680]:


df["case number"]=caseno


# In[681]:


erflist = []


# In[682]:


for url in df['url']:
    #print(url)
    #page=urllib.request.urlopen(url).read().decode().lower()
    match = re.search('erf (\d+)', urllib.request.urlopen(url).read().decode().lower())
    if match and len(match.group(1))>2:
        erflist.append(match.group(1))
        #print (match.group(1))
    else:
        erflist.append("not find ERF number")


# In[683]:


df['erf'] = erflist


# In[684]:


hearddate = []


# In[685]:


for url in df['url']:
    print(url)
    ny_bb = url_to_string(url)
    article = str(nlp(ny_bb))
    #page=urllib.request.urlopen(url).read().decode().lower()
    match1 = re.search('hearing: ([^.]+|\S+)', article.lower())
    match2 = re.search('heard: ([^.]+|\S+)', article.lower())
    if match1 and len(match1.group(1))>2:
        #erflist.append(match.group(1))
        text = str(match1.group(1))
        #print(text)
        alldate = re.search(r"((?:\S+\s+){0,2}\b2018)",text)
        print(alldate.group(1))
        hearddate.append(alldate.group(1))
    elif match2 and len(match2.group(1))>2:
        #erflist.append(match.group(1))
        text = str(match2.group(1))
        #print(text)
        alldate = re.search(r"((?:\S+\s+){0,2}\b2018)",text)
        print(alldate.group(1))
        hearddate.append(alldate.group(1))
    
    else:
        hearddate.append("not find heard date")


# In[686]:


df['heard date']=hearddate


# In[687]:


caseaddress = []


# In[688]:


for url in df['url']:
    temmatch = []
    page=urllib.request.urlopen(url).read().decode().lower()
    print(url)
    if 'situated' in page:
        print("has situated")
        ny_bb = url_to_string(url)
        article = nlp(ny_bb)
        sentences = [x.text for x in article.sents]
        for senten in sentences:
            if 'situated' in str(senten.lower()):
                match = re.search(r'situated\s+(.*)', str(senten))
                if match and match.group(1).startswith("at") and len(match.group(1))>8:
                    #print(senten)
                    temmatch.append(match.group(1))
                    print(match.group(1))
                elif match and match.group(1).startswith("in") and len(match.group(1))>8:
                    #print(senten)
                    print(match.group(1))
                    temmatch.append(match.group(1))
                elif match and match.group(1).startswith("on") and len(match.group(1))>8:
                    #print(senten)
                    print(match.group(1))
                    temmatch.append(match.group(1))
                    
    if ' road' in page:
        #print(url)
        print( "has road")
        ny_bb = url_to_string(url)
        article = nlp(ny_bb)
        sentences = [x.text for x in article.sents]
        for senten in sentences:
            if ' road' in str(senten.lower()):
                match = re.search(r"((?:\S+\s+){0,1}\broad)",str(senten.lower()))
                if not match.group(1).split(' ', 1)[0] in stop_words:
                    #print(senten)
                    print(match.group(1))
                    temmatch.append(match.group(1))
                
    if ' street' in page:
        #print(url)
        print( "has street")
        ny_bb = url_to_string(url)
        article = nlp(ny_bb)
        sentences = [x.text for x in article.sents]
        for senten in sentences:
            if ' street' in str(senten.lower()):
                match = re.search(r"((?:\S+\s+){0,1}\bstreet)",str(senten.lower()))
                if not match.group(1).split(' ', 1)[0] in stop_words:
                    #print(senten)
                    print(match.group(1))
                    temmatch.append(match.group(1))
                    
    if ' avenue' in page:
        #print(url)
        print( "has Avenue")
        ny_bb = url_to_string(url)
        article = nlp(ny_bb)
        sentences = [x.text for x in article.sents]
        for senten in sentences:
            if ' avenue' in str(senten.lower()):
                match = re.search(r"((?:\S+\s+){0,1}\bavenue)",str(senten.lower()))
                if not match.group(1).split(' ', 1)[0] in stop_words:
                    #print(senten)
                    print(match.group(1))
                    temmatch.append(match.group(1))
    if temmatch:
        caseaddress.append(temmatch[0])
    if not temmatch:
        caseaddress.append("not find address")


# In[689]:


df['address'] = caseaddress


# In[690]:


df['year'] = yearinput


# In[691]:


MyEmptydf=MyEmptydf.append(df)


# In[692]:


MyEmptydf


# In[693]:


with pd.ExcelWriter(r'C:\Users\yyjia\Desktop\sjcdata\pie.xlsx') as writer:
    MyEmptydf.to_excel(writer, index = None, header=True)

