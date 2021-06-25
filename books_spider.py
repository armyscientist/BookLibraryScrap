from mysql.connector import connection
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

import mysql.connector
from fuzzywuzzy import fuzz
import regex as re

class BooksSpider(scrapy.Spider):
    name='GoodReads'
    
    #allowed_domains = 'goodreads.com'   
    #start_urls=['https://www.goodreads.com/search?q=wings+of+fire']   
    def __init__(self):
        self.connection=mysql.connector.connect(
                pool_name = "mypool",
                pool_size = 1,
                host='localhost',
                user='root',
                passwd='ma5t3rb1a5t3r',
                database='hnelibrary',
                autocommit=True
            )
        
        self.cursor=self.connection.cursor(buffered=True)    

    def start_requests(self):      
        
        self.cursor.execute("SELECT ID, Title, Author FROM tblbookinfo WHERE ID BETWEEN 1103 AND 1130")  
        for row in self.cursor:
            title=row[1].replace(' ','+')
            print("&&&&&&&ID = ",row[0],"Preparing 1st request")
            author=row[2].split()
            print("**Yielding 1st request")
            yield scrapy.Request('https://www.goodreads.com/search?utf8=2%9C%93&query={}'.format(title),
                                    callback=self.parse,
                                    cb_kwargs={'ID':row[0],'book_title':row[1],'book_author':row[2]},
                                    errback=self.errback_httpbin,
                                    dont_filter=False)
        
            
               
    def parse(self, response, ID, book_title, book_author):                  
        #print("IDIDIIDIDIDIDIIDID=",ID,"******************")
        result_status=response.css(".searchSubNavContainer::text").get()
        if(result_status=="No results."):
            print("&&&&&&&ID = ",ID,"$$No Result")
            return
        search_results=response.css('tr')        
        title=search_results.css(".bookTitle span::text").extract()        
        author=[book.css(".authorName span::text").extract() for book in search_results]               
        url=search_results.css(".bookTitle::attr(href)").extract()      
        #print("************",title,'*****************',author,'*************',url) 
        #wrong logic
        '''rank={}
        for i in range(len(title)):
            maxmin=[]
            for j in author[i]:
                maxmin.append(fuzz.token_sort_ratio(j, book_author))
            maxmin=max(maxmin)
            rank[i]=fuzz.partial_ratio(title[i].lower(),book_title.lower())/maxmin   
        print("**Rank list is ready!",rank)
        keys=list(rank.keys())
        maxmin=keys[0]
        for i in keys:
            if(rank[maxmin]>rank[i]):
                    maxmin=i'''  
        #alternate logic     
        #print("&&&&&&&&&&&&&&&&&&&&",book_author)
        book_author=book_author.split(', ')
        rank=-1
        m,a, nba=0,0,len(book_author)        
        #book_author_tokens=book_author.lower().split()
        #print("&&&&&&&&&&&&&&&&&&&&",type(book_author))
        for i in range(len(book_author)):
            
            book_author[i]=re.split(r'\W',book_author[i].lower()) 
            book_author[i]=list(filter(lambda x: bool(x), book_author[i]))
        print("**",book_author)

        for i in range(len(title)):            
            
            if(fuzz.partial_ratio(title[i].lower(),book_title.lower())==100):                
                res_author=author[i]
                nra=len(res_author)

                for k in range(nra):
                    res_author[k]=re.split(r'\W',str(res_author[k]).lower()) 
                    res_author[k]=list(filter(lambda x: bool(x), res_author[k]))
                print("****",res_author)

                for per_book_author in book_author:
                    for per_res_author in res_author:              
                        for name in per_book_author:
                            m+=per_res_author.count(name)
                            print("*m=",m)
                        
                        if(m==len(per_book_author) or m>=2):
                            a+=1
                            break
                        else:
                            m=0 
                    #print("&&",m)
                        
                if(a):                     
                    rank=i
                    break
                    
        if(rank!=-1):       
        #self.cursor.execute("UPDATE tblbookinfo SET href={0} WHERE ID={1}".format(url[maxmin], ID))      
            print("**Yielding 2nd request")   
            url='https://www.goodreads.com'+str(url[rank])
            self.cursor.execute("UPDATE tblbookinfo SET URL=(%s) WHERE ID=(%s);",(url, ID)) 
            print("&&&&&&&ID = ",ID,"$$Found")    
            yield scrapy.Request(url, callback=self.parse_description,
                                        cb_kwargs={'ID':ID},
                                        errback=self.errback_httpbin,
                                        dont_filter=False)
        else:
            print("&&&&&&&ID = ",ID,"Not Found")
            return


    def parse_description(self, response, ID):
        print("**Responded 2nd request")   
        genre=response.css(".left .bookPageGenreLink::text").extract()        
        genre=', '.join(map(str, genre))
        description=response.css("#description span::text").extract()       
        #print("***",description, genre) 
        if(len(description)==2):
            del description[0]
        if(not description):
            description=None
        else:
            description=str(description[0])
        
        #print("**Extracted data ***************** Connection",self.cursor, self.connection) 
                   
        self.cursor.execute("UPDATE tblbookinfo SET Description=(%s), Genre=(%s) WHERE ID=(%s);",(description, genre, ID))
        #self.connection.commit()
        print("**Updated database")        
        
        
        
    #def parse_httpbin(self, response):
    #    self.logger.info('Got successful response from {}'.format(response.url))
        # do something useful here...

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)


    







        

            





