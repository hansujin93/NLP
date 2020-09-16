forum_url = "https://www.mumsnet.com/Talk/toys_and_games_chat/3414974-noisy-baby-toys-which-are-the-worst?pg=1"
#load webpage
req = requests.get(forum_url)
#Use beautiful soup to decode webpage text into parseable document.
soup = BeautifulSoup(req.text, "html.parser")
msgs = soup.find_all('div', {'class': 'talk-post'})
good_bad = {'good':0, 'bad':0}

posts = []
for msg in msgs:
    for href in msg.select('a[href]'):
        href.decompose()
    post = msg.find('p')
    for br in post.find_all("br"):
        br.replace_with("\n")
    plain_post = re.sub('[^a-zA-Z,\s0-9\']','',post.text)  
    plain_post = plain_post.replace('  ',' ')
    par = justext.justext(post.text, justext.get_stoplist('English'))
    for p in par:
        if p.class_type == 'good':
            good_bad['good'] += 1
        else:
            good_bad['bad'] += 1
    posts.append(plain_post.strip())
        
with open('forum_result.txt', 'w') as f:
    for pp in posts:
        f.write("%s\n" % pp.replace("\n", "  ").replace("\r", "  "))
