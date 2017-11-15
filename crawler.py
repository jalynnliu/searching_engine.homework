#!/usr/bin/python
from spdUtility import PriorityQueue,Parser
import urllib2
import sys
import os
import inspect
import time
g_url = 'http://www.sina.com.cn'
g_key = 'www'
"""
def line():
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back.f_lineno"""

def updatePriQueue(priQueue, url):
    extraPrior = url.endswith('.html') and 2 or 0 
    extraMyBlog = g_key in url and 5 or 0 
    item = priQueue.getitem(url)
    if item:
        newitem = (item[0]+1+extraPrior+extraMyBlog, item[1])
        priQueue.remove(item)
        priQueue.push(newitem)
    else :
        priQueue.push( (1+extraPrior+extraMyBlog,url) )
        
def getmainurl(url):
    ix = url.find('/',len('http://') )
    if ix > 0 :
        return url[:ix]
    else :
        return url
def analyseHtml(url, html, priQueue, downlist):
    p = Parser()
    try :
        p.feed(html)
        p.close()
    except:
        return
    mainurl = getmainurl(url)
    print mainurl
    for (k, v) in p.anchors.items():
        for u in v :
            if not u.startswith('http://'):    
                u = mainurl + u
            if not downlist.count(u):
                updatePriQueue( priQueue, u)
                
def downloadUrl(id, url, priQueue, downlist,downFolder):
    downFileName = downFolder+'/%d.html' % (id,)
    print 'downloading', url, 'as', downFileName, time.ctime(),
    try:
        fp = urllib2.urlopen(url)
    except:
        print '[ failed ]'
        return False
    else :
        print '[ success ]'
        downlist.push( url )
        op = open(downFileName, "wb")
        html = fp.read()
        op.write( html )
        op.close()
        fp.close()
        analyseHtml(url, html, priQueue, downlist)
        return True

def spider(beginurl, pages, downFolder):
    priQueue = PriorityQueue()
    downlist = PriorityQueue()
    priQueue.push( (1,beginurl) )
    i = 0
    while not priQueue.empty() and i < pages :
        k, url = priQueue.pop()
        if downloadUrl(i+1, url, priQueue , downlist, downFolder):
            i += 1
    print '\nDownload',i,'pages, Totally.'

def main():
    beginurl = g_url
    pages = 20000
    downloadFolder = './spiderDown'
    if not os.path.isdir(downloadFolder):
        os.mkdir(downloadFolder)
    spider( beginurl, pages, downloadFolder)

if __name__ == '__main__':
    main()
