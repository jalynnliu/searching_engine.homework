def get_page(url):  
    try:  
        import urllib.request 
        page=urllib.request.urlopen(url)  
        html=page.read()  
        return html  
    except:  
        return ""  

def get_next_target(page):  
    
    start_link=page.find('<a href=')  
    if start_link == -1:  
        url=''
        end_quote=0  
    else:
        start_quote=page.find('"',start_link) 
        end_quote=page.find('"',start_quote+1)  
        url=page[start_quote+1:end_quote]  
    return url,end_quote  

def get_all_links(page):  
    links=[]  
    while True:  
        url,endpos=get_next_target(page)  
        if url:  
            links.append(url)  
            page=page[endpos:]  
        else:  
            break  
    return links  

def union(a,b):  
    for e in b:  
        if e not in a:  
            a.append(e)  

def crawl_web(seed):    #return index,graph of links  
    tocrawl =[seed]  
    crawled=[]  
    graph={} #<url>, [list of pages it links to]  
    index={}  
    while tocrawl:  
        page = tocrawl.pop()  
        if page not in crawled:  
            content=get_page(page)
            content=bytes.decode(content)  
            add_page_to_index(index,page,content)  
            outlinks=get_all_links(content)  
            graph[page]=outlinks  
            union(tocrawl,outlinks)  
            crawled.append(page)  
    return index,graph  

#---------------------------------build_index------------------------------------  
def add_page_to_index(index,url,content):  
    words=content.split()  
    for word in words:  
        add_to_index(index,word,url)  

def add_to_index(index,keyword,url):  
    if keyword in index:  
        index[keyword].append(url)  
    else:  
        index[keyword]=[url]  

def lookup(index,keyword):  
    if keyword in index:  
        return index[keyword]  
    else:  
        return None  

#---------------------------------page_rank------------------------------  

def compute_ranks(graph):  
    d=0.8 #damping facotr  
    numloops= 10 
    ranks={}  
    npages=len(graph)  
    for page in graph:  
        ranks[page]=1.0/npages  
    for i in range(0,numloops):  
        newranks={}  
        for page in graph:  
            newrank=(1-d)/npages  
            for node in graph:  
                if page in graph[node]:  
                    newrank=newrank+d*(ranks[node]/len(graph[node]))  
            newranks[page]=newrank  
        ranks=newranks  
    return ranks  

def quick_sort(url_lst,ranks):  
    url_sorted_worse=[]  
    url_sorted_better=[]  
    if len(url_lst)<=1:  
        return url_lst  
    pivot=url_lst[0]  
    for url in url_lst[1:]:  
        if ranks[url]<=ranks[pivot]:  
            url_sorted_worse.append(url)  
        else:  
            url_sorted_better.append(url)  
    return quick_sort(url_sorted_better,ranks)+[pivot]+quick_sort(url_sorted_worse,ranks)  

def ordered_search(index,ranks,keyword):  
    if keyword in index:  
        all_urls=index[keyword]  
    else:  
        return None  
    return quick_sort(all_urls,ranks)  
  
#------------------------------test-------------------------  
if __name__=='__main__':  
    index,graph=crawl_web('http://www.baidu.com/')  
    ranks=compute_ranks(graph)  

    ranked_urls=ordered_search(index,ranks,'baidu')  
    for i,url in enumerate(ranked_urls):  
        print("(%d),%s",(i,url))  
