lastpage = re.compile(r"page\s(\d+)(\s)of\s(\d+)") #compiled regular expression, checking if we're at page n of n, i.e. last page.
#..
pages = soup.find('div', {'class': 'pages'}).text.strip() #find pages element which has the "This is page x of y" text.

#if lastpage.search(pages) != None: #if our regex matches, then we're on last page, so make this the last one to parse.
#    at_last = True

ppg = soup.find('div', {'class': 'pages'}).find('p').text
result = lastpage.search(ppg)
last_pp = result.group(3)
print(last_pp)
