#---*----coding:utf-8---*----
import urllib2,unittest,re
import codecs
from BeautifulSoup import BeautifulSoup
class BDTBTestCase(unittest.TestCase):
    ######################测试程序begin######################
    #####测试用常量
    baseUrlPre=r"http://tieba.baidu.com/p/"
    TIEBAID=r"4514775546"
    see_lzPre=r"?see_lz="
    see_lz=0                      #1：只看楼主0：所有都看
    pnPre=r"&pn="
    pn = 1
    url=r"http://tieba.baidu.com/p/4514775546"
    def testGetPage(self):
        flag = 'waiting'
        bdtd = BDTB(self.url,0)
        page = bdtd.getPage(1)
        #测试getTitle函数
        title =bdtd.getTitle(page)        
        self.failUnless(title == u'买了kindle后有每天都看书么_kindle吧_百度贴吧',"title get failed!")
        #测试getLouAndPageNum函数
        louAndPage = bdtd.getLouAndPageNum(page)
        
        self.assertEqual(int(louAndPage['loutalnum'])> 128,True)
        
        self.assertEqual(int(louAndPage['pagenum']) >= 3,True)
        #测试getLouContent函数
        contentlist = bdtd.getLouContent(int(louAndPage['pagenum']))
        for i in contentlist:
            if i:
                if u"每天都会阅读但不一定用kindle" in i:
                    flag = 'ok'                    
        self.assertEqual(flag,'ok')
        #测试write函数：
        
        filename = bdtd.writeFile(title,contentlist)
        self.assertEqual(filename,u'买了kindle后有每天都看书么_kindle吧_百度贴吧.txt')
        ######################测试程序end######################





        
        

#####执行类
class BDTB():
    
    def __init__(self,baseUrl,see_lz):
        see_lzPre=r"?see_lz="
        pnPre=r"&pn="
        
        print see_lzPre,pnPre
        self.baseUrl=baseUrl
        
        self.see_lzPre = see_lzPre
        self.see_lz=see_lz
        self.pnPre = pnPre
        
    def getPage(self,pn):
        print "getPage()"
        url = self.baseUrl+self.see_lzPre+str(self.see_lz)+self.pnPre+str(pn)
        request = urllib2.Request(url)
        page = urllib2.urlopen(request).read()
        return page
    def getTitle(self,page):
        print "getTitle()"
        titleBS=BeautifulSoup(page).find('title')
        title = titleBS.string
        return title
    def getLouAndPageNum(self,page):
        print "getLouAndPageNum(self,page)"
        dirs = {'loutalnum':0,'pagenum':0}     
        loutotalnumBS =BeautifulSoup(page).find('li',attrs={'class':'l_reply_num'})
        if loutotalnumBS:
            loutotalnumBSspans = loutotalnumBS.findAll('span')
            dirs['loutalnum']=int(loutotalnumBSspans[0].string)
            dirs['pagenum']=int(loutotalnumBSspans[1].string)
            print dirs
        return dirs
    def getLouContent(self,totalPage):
        #设定class的正则匹配规则
        pat = re.compile(r'post_content_.*')
        print "getLouContent(totalPage)"
        contentlist =[]
        #获取所有楼层的东西到contentlist里面去，并返回
        for index in range(1,totalPage+1):
            page = self.getPage(index)
            contentBS = BeautifulSoup(page).findAll('div',attrs={'id':pat})
            #print contentBS
            for content in contentBS:
                contentlist.append(content.string)
        return contentlist
    def writeFile(self,title,contentlist):   
        print "writeFile(self,title,contentlist)"
        p= re.compile(r'[^._…]*')
        shortTitle = p.match(title).group()
        print shortTitle
        filename = shortTitle+".txt"
        with codecs.open(filename,'w','utf-8') as f:
            header = "-------"+title+"-------"
            f.write(header+'\n')
            for index,line in enumerate(contentlist):
                lou = u"【{index}楼】".format(index=index+1)
                f.write(lou+'\n')
                print lou
                if line:
                    f.write(line+'\n')
                    print line
        return filename,shortTitle
    def start(self):
        page = self.getPage(1)
        dirs = self.getLouAndPageNum(page)
        title = self.getTitle(page)
        contentlist = self.getLouContent(dirs['pagenum'])
        filename,shortTitle = self.writeFile(title,contentlist)
        print u"生成{shortTitle}txt文件，请查看".format(shortTitle=shortTitle)
        return contentlist
             
            
            
            


if __name__=="__main__":
##测试用例入口，当执行unittest.main结束后，整个函数直接返回，不会继续执行后面的语句，使用时请注释
##    unittest.main()
    while(1):
        print u"请输入帖子代号"
        tieBaID=raw_input()
        print u"是否只看楼主，1是，0否"
        see_lz=raw_input()
        url=r"http://tieba.baidu.com/p/"+tieBaID
        bdtb = BDTB(url,see_lz)
        contentlist = bdtb.start()
 
    
