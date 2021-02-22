# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import datetime


# 请求连接
def get_data(link):
    try:
        r = requests.get(link, timeout=15)
        r.encoding = 'utf-8-sig'
        result = r.text
    except:
        print('请求超过15s。')
    return result

def matery_get_friendlink(friendpage_link, friend_poor):
    result = get_data(friendpage_link)
    soup = BeautifulSoup(result, 'html.parser')
    main_content = soup.find_all('div', {"class": "friend-div"})
    for item in main_content:
        img = item.find('img').get('src')
        link = item.find('a').get('href')
        name = item.find('h1').text
        if "#" in link:
            pass
        else:
            user_info = []
            user_info.append(name)
            user_info.append(link)
            user_info.append(img)
            print('----------------------')
            try:
                print('好友名%r' % name)
            except:
                print('非法用户名')
            print('头像链接%r' % img)
            print('主页链接%r' % link)
            friend_poor.append(user_info)

# 从butterfly主页获取文章
def get_last_post_from_butterfly(user_info,post_poor):
            error_sitmap = 'false'
            link = user_info[1]
            print('\n')
            print('-------执行主页规则----------')
            print('执行链接：', link)
            result = get_data(link)
            soup = BeautifulSoup(result, 'html.parser')
            main_content = soup.find_all(id='recent-posts')
            time_excit = soup.find_all('time')
            if main_content and time_excit:
                error_sitmap = 'true'
                link_list = main_content[0].find_all('time', {"class": "post-meta-date-created"})
                if link_list == []:
                    print('该页面无文章生成日期')
                    link_list = main_content[0].find_all('time')
                else:
                    print('该页面有文章生成日期')
                lasttime = datetime.datetime.strptime('1970-01-01', "%Y-%m-%d")
                for index, item in enumerate(link_list):
                    time = item.text
                    time = time.replace("|","")
                    time = time.replace(" ", "")
                    if lasttime < datetime.datetime.strptime(time, "%Y-%m-%d"):
                        lasttime = datetime.datetime.strptime(time, "%Y-%m-%d")
                lasttime = lasttime.strftime('%Y-%m-%d')
                print('最新时间是', lasttime)
                last_post_list = main_content[0].find_all('div', {"class": "recent-post-info"})
                for item in last_post_list:
                    time_created = item.find('time', {"class": "post-meta-date-created"})
                    if time_created:
                        pass
                    else:
                        time_created = item
                    if time_created.find(text=lasttime):
                        error_sitmap = 'false'
                        print(lasttime)
                        a = item.find('a')
                        # print(item.find('a'))
                        alink = a['href']
                        alinksplit = alink.split("/", 1)
                        stralink = alinksplit[1].strip()
                        if link[-1] != '/':
                            link = link + '/'
                        print(a.text)
                        print(link + stralink)
                        print("-----------获取到匹配结果----------")
                        post_info = {
                            'title': a.text,
                            'time': lasttime,
                            'link': link + stralink,
                            'name': user_info[0],
                            'img': user_info[2]
                        }
                        post_poor.append(post_info)
            else:
                error_sitmap = 'true'
                print('貌似不是类似butterfly主题！')
            print("-----------结束主页规则----------")
            print('\n')
            return error_sitmap