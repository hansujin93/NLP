base_url = "https://en.wikipedia.org/wiki/Filmography_and_awards_of_Stanley_Kubrick"
#load webpage
req = requests.get(base_url)
#Use beautiful soup to decode webpage text into parseable document.
soup = BeautifulSoup(req.text, "html.parser")

table = soup.find('table', {'class': 'wikitable'}) #just find 1 table, as it's the first 1
trs = table.findAll('tr')[1:]  #skip headtrs = table.find_all('tr')[1:]


answer = []
for tr in trs:
    try:
        year = int(tr.findChildren()[0].text)
        title = tr.findChildren()[1].text.strip()
    except ValueError:
        year = answer[-1][0]
        title = tr.findChildren()[0].text.strip()
    answer.append([year,title])
    
with open('wikipedia_result.json', 'w') as f:
    json.dump(answer, f, indent=4)
