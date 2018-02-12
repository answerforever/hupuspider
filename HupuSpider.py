#coding=utf-8
import requests
from bs4 import BeautifulSoup
import datetime
import sys
from MongoApi import MongoAPI

def get_page(link):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    r=requests.get(link,headers=headers)
    #r.encoding = r.apparent_encoding
    print(r.encoding)
    html=r.content
    #html=html.decode('UTF-8')
    soup=BeautifulSoup(html,'lxml')
    print(soup.original_encoding)
    #soup=BeautifulSoup(html,'html.parser')
    print(soup)
    print(sys.getfilesystemencoding())
    return soup

def get_data(post_list):
    data_list=[]
    for post in post_list:
        title_td=post.find('div',class_='titlelink')
        title=title_td.find('a',class_='truetit').text.strip()
        post_link=title_td.find('a',class_='truetit')['href']
        post_link='https://bbs.hupu.com'+post_link
        author_td=post.find('div',class_='author')
        author=author_td.find('a',class_='aulink').text.strip()
        author_page=author_td.find('a',class_='aulink')['href']
        start_date=author_td.find_all('a')[1].text
        start_date=datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
        reply_view=post.find('span',class_='ansour').text.strip()
        reply=reply_view.split('/')[0].strip()
        view=reply_view.split('/')[1].strip()
        reply_time=post.find('div',class_='endreply')
        last_reply=reply_time.find('a').text.strip()
        if ':' in last_reply:
            date_time=str(datetime.date.today())+' '+last_reply
            date_time=datetime.datetime.strptime(date_time,'%Y-%m-%d %H:%M')
            data_list.append([title,post_link,author,author_page,start_date,reply,view,date_time])
        elif(len(last_reply)==10):
            date_time=datetime.datetime.strptime(last_reply,'%Y-%m-%d').date()
            data_list.append([title,post_link,author,author_page,start_date,reply,view,date_time])       
        else:
            date_time=datetime.datetime.strptime('2018-'+last_reply,'%Y-%m-%d').date()
            data_list.append([title,post_link,author,author_page,start_date,reply,view,date_time])
    return data_list

hupu_post=MongoAPI("192.168.10.178",27017,"Spider","HupuInfo")
for i in range(1,101):
    link="https://bbs.hupu.com/realmadrid-"+str(i)
    soup=get_page(link)
    main=soup.find('ul',class_='for-list')
    post_list=main.find_all('li')
    data_list=get_data(post_list)
    #with open('E:\\TestProject\\SpiderTest\\title.txt',"a+") as f:
        #for each in data_list:
            #print(each[0])
            #f.writelines(each[0])
    #f.close()
    for each in data_list:
        hupu_post.add({"title":each[0],
        "post_link":each[1],
        "author":each[2],
        "author_page":each[3],
        "start_date":str(each[4]),
        "reply":each[5],
        "view":each[6],
        "post_link":each[1]})
#time.sleep(3)
print('第',i,'页获取完成，休息3秒')


#for each in data_list:
    #print (each)

          