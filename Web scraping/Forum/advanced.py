lastpage = re.compile(r"page\s(\d+)(\s)of\s(\d+)") #compiled regular expression, checking if we're at page n of n, i.e. last page.
#..
pages = soup.find('div', {'class': 'pages'}).text.strip() #find pages element which has the "This is page x of y" text.

#if lastpage.search(pages) != None: #if our regex matches, then we're on last page, so make this the last one to parse.
#    at_last = True

ppg = soup.find('div', {'class': 'pages'}).find('p').text
result = lastpage.search(ppg)
last_pp = result.group(3)
print(last_pp)


posts = []
lastpage = re.compile(r"page\s(\d+)(\s)of\s(\d+)")
ppg = soup.find('div', {'class': 'pages'}).find('p').text
lastpage_num = int(lastpage.search(ppg).group(3))

startpost = 0
for i in range(1, lastpage_num+1):
    if i > 1:
        startpost = 1
    pageload = {'pg': i}
    r = requests.get('https://www.mumsnet.com/Talk/toys_and_games_chat/3414974-noisy-baby-toys-which-are-the-worst'
                 , params=pageload)
    soup = BeautifulSoup(r.text, "html.parser")
    msgs = soup.find_all('div', {'class': 'talk-post'})
    
    for m in range(startpost, len(msgs)):
        for href in msgs[m].select('a[href]'):
            href.decompose()
        post = msgs[m].find('p')
        for br in post.find_all("br"):
            br.replace_with("\n")
        plain_post = re.sub('[^a-zA-Z ,0-9]','',post.text)  
        plain_post = plain_post.replace('  ',' ')
        posts.append(plain_post.strip())

with open('forum_result_advanced.txt', 'w') as f:
    for pp in posts:
        f.write("%s\n" % pp.replace("\n", "  ").replace("\r", "  "))
