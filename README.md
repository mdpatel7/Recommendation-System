# Recommendation-System
Python, AWS Elastic Search

I have built a web crawler in python using the beautiful soup library.	
Beautiful soup parses HTML and XML documents and creates a parse tree to get data from HTML tags.	
I have scraped data from Java wikibooks as well as Oracle Documents into .csv files. I have submitted two python files which crawls JavaWikibooks and Oracle documents.	
	
Indexing
				
I have used Amazon Web Service's ElasticSearchService which is built on top of Lucene for indexing my crawled content.	
Registering with ElasticSearchService provides an API end-point which we can be used to push the crawled data.
I have pushed the crawled data(both java wikibooks and Orace Docs) through the python script to the elastic search.
Elasticsearch service uses Inverted Index technique which consists of collection of unique words in each document and all the documents in which that word appears.
Elasticsearch applies analyzer to the textfields, results of which are 		stored in inverted index.
Elastic search creates indices of the number of records(rows in my .csv). 
Index in Elastic Search is a kind of a database in MySQL.
An Elasticsearch cluster contains Indices (databases), which in turn contain multiple Types (tables). These types hold multiple Documents (rows), and each document has Properties(columns).
I created an Ajax get query to call the ElasticSearch API and displayed the response data in my front end.
