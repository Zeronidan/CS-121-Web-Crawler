# CS-121-Web-Crawler
A web crawler we created in CS 121: Information Retrieval class at UCI.  Collaborated with Alicia Xu.


Technologies Used: 
- Python
- BeautifulSoup


The program reads a bookkeeping.tsv file that stores the webpages to crawl.  It uses BeautifulSoup to parse and extract HTML content, creating an term-document frequency index that stores a series of (term, webpage, term frequency). 


Once the inverted index of term and documents is created, the user is prompted to enter a query.  The program generates and ranks the top 5 webpages that contain the query.
