import fuzzywuzzy as fuzz
import regex as re

book_author=['Nandedkar R. Y.', 'Rajadhyaksha I. O.']
title=['hello']
author=[['y Nandedkar', 'o Rajadhyaksha']]
rank=-1
m,a, nba=0,0,len(book_author)      
  
#book_author_tokens=book_author.lower().split()

for i in range(len(book_author)):
    print(book_author[i])
    book_author[i]=re.split(r'\W',str(book_author[i]).lower()) 
    book_author[i]=list(filter(lambda x: bool(x), book_author[i]))
print("**",book_author)

for i in range(len(title)):     
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
        print("&&",m)
            
    if(a==nba):
        rank=i
        break
print(rank)

