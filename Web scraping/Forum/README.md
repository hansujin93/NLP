The optional lab workbook uses Scrapy to download pages from a forum, a similar task can be performed for forums with Requests and Beautiful Soup. 
Choose any forum and use what you've learnt to parse thread posts into plain text. 
Start with an individual thread, and one page of posts within that thread.\

<b>Advanced:</b>
The topic's posts are spread across multiple pages, this means that "paging" needs to be performed to extract the posts from every page. 
Need to consult the requests documentation to discover how to pass parameters to match the links to other pages.
Be careful not to have duplicate posts in your extraction (the original post is repeated on each page).
