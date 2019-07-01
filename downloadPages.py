#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import bs4
from mxp.utils import * 
import sys

def geturl(url):
    return requests.get(url);

def geturl2file(url, fn):
    with open(fn,'w') as f:
        f.write(geturl(url).text)

def main():
    url = 'http://glslsandbox.com/?page=0'
    geturl2file(url,'/tmp/tt.html')

def getAllShaderUrlFromHtml(html):
    try: 
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup
    parsed_html = BeautifulSoup(html, features="html.parser")
    gallery= parsed_html.find_all('div',{'id':'gallery'})
    if gallery == None: return []
    else:
        shaders = []
        print gallery, '29'
        for a in gallery[0].find_all('a'):
            shaderurl =  a['href']
            imgurl = a.find_all('img')[0]['src']
            print shaderurl, imgurl
            shaders.append((shaderurl, imgurl))
        return shaders

def updateAllPagesHtml():
    # down all page in here
    if fileExist("datas/allPageShaderInfo.json"):
        allPageShaderInfo = json.load(open('datas/allPageShaderInfo.json'))
    else:
        allPageShaderInfo = {}
    for i in range(100000):
        print i
        fn = 'datas/page.htmls/%d.html' % i
        if not fileExist(fn):
            createDirForFn(fn)
            url = 'http://glslsandbox.com/?page=%d' % i
            print url, fn
            geturl2file(url, fn)
        shaderUrls = getAllShaderUrlFromHtml(open(fn).read())
        if len(shaderUrls)==0:break;
        allPageShaderInfo[str(i)] = shaderUrls
    saveJson2File(allPageShaderInfo,'datas/allPageShaderInfo.json')
        

def main0():
    page=1000000
    url = 'http://glslsandbox.com/?page=%d' % page
    geturl2file(url, '/tmp/tt.html')
    #shaderUrls = getAllShaderUrlFromHtml(open('/tmp/tt.html').read())
    shaderUrls = getAllShaderUrlFromHtml(open('datas/page.htmls/0.html').read())
    #if len(shaderUrls)==0:break;
    print shaderUrls

def updateAllShaderandImageUrls():
    #updateAllPagesHtml()
    #  get all shaders
    allPageShaderInfo = json.load(open('datas/allPageShaderInfo.json'))
    allShaderurls = []
    allImageUrls = []
    for k,v in allPageShaderInfo.items():
        shaders =  v
        for shaderurl, imageurl in shaders:
            print shaderurl
            allShaderurls.append(shaderurl);
            allImageUrls.append(imageurl)
    saveJson2File(allShaderurls, 'datas/allShaderurls.json')
    saveJson2File(allImageUrls, 'datas/allImageUrls.json')

def main():
    allShaderurls = json.load(open('datas/allShaderurls.json'))
    for url in allShaderurls:
        if url.startswith('/e#'): url =url[3:]
        durl = 'http://glslsandbox.com/item/%s' % url
        dfn = 'datas/shaders/%s.json' %url
       
        createDirForFn(dfn)
        print durl, dfn
        if fileExist(dfn): continue
        geturl2file(durl, dfn)

    

if __name__ == '__main__':
    # some initialization code
    reload(sys)
    sys.setdefaultencoding('utf8')

    main()

