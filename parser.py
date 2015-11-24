import feedparser
import urllib.parse
import re
import csv
import jieba
import random

"""Change to Traditional Chinese dictionary and self-defined dictionary"""
#code
# jieba.set_dictionary('dict.txt.big')
# jieba.load_userdict("userdict.txt")




"""Build dictionary where (key, value) = (country/city name, locations) from existing file"""
dict_country_to_geolocation = dict()
with open('country_city_location.csv', "r", newline = '', encoding = 'utf8') as geofile:
    georeader = csv.reader(geofile, delimiter=',' )
    for terms in georeader:
        dict_country_to_geolocation[terms[0]] = (terms[1], terms[2])

# check dictionary result
# for key, value in dict_country_to_geolocation.items():
#     print(key , " = " , dict_country_to_geolocation[key])



"""Prompt for user interest"""
# is_topic = input("是否指定主題(Y/N):")
# if is_topic == 'Y' or is_topic == 'y':
#   topic = input("國際=w 台灣=n 財經=b 科技=t 體育=s 娛樂=e 兩岸=c 社會=y 健康=m: ")
#   vaild = re.compile(r"[wnbtsecym]")
#   if vaild.search(topic) is None:
#       topic = ""


"""Parse chinese characters into url"""
query = ""
query = input("我想知道關於: ")
query = query.encode('utf8')
query = urllib.parse.quote(query)

#Google News RSS
url_request = 'https://news.google.com.tw/news?cf=all&hl=zh-TW&pz=1&ned=us&q=' + query + '&output=rss' \
            + '&tbs=qdr:d,sbd:1' + '&tbm=nws' + 'source=lnt&sa=X' + '&biw=1779&bih=951&dpr=1'

if query == '':
    url_request += '&topic=w'

#地球圖輯隊RSS
url_request_yam = 'http://world.yam.com/rss.php'


# print(url_request)
# print(repr(query))

# if is_topic == 'Y' or is_topic == 'y':
#   topic_url = '&topic=' + topic
#   url_request +=  topic_url

# f = feedparser.parse(r'test_feed.rss')
# f = feedparser.parse('https://news.google.com.tw/news?cf=all&hl=zh-TW&pz=1&ned=us&q=%22%E5%8F%B0%E7%81%A3%22+OR+%22%E6%B3%95%E5%9C%8B%22&output=rss')
f = feedparser.parse(url_request)

# print(f.feed)

print(f.feed.title + " (" + f.feed.published + ")")

"""Process 10 most recently fetched feeds and store the result into file iteratively"""
with open('feed.csv', 'w', newline = '', encoding = 'utf8') as csvfile:
    feedwriter = csv.writer(csvfile, delimiter=",", lineterminator='\n')
    feedwriter.writerow(["Feed ID"] + ["Title"] + ["Published Time"] + ["Link"] + ["longitude"]
                                    + ["latitude"])

    #Just want to make the jieba message show faster
    temp = jieba.lcut_for_search(f.feed.title)

    for i, val in enumerate(f.entries):
        """Show feed on the standard output"""
        # print(val.summary_detail.value)
        print(str(i + 1) + ". " + val.title)


        """Parse chinese title and/or content to fetch contury related terms using jieba lib"""

        title_term_list = jieba.lcut_for_search(val.title) #search model
        # for term in title_term_list:
        #         print(term, end = " ")
        # print()

        """Geolocation initialization"""
        longitude = ""
        latitude = ""

        """find key term for geolocation including country/city names, important sites"""
        keyterm = ""
        for term in title_term_list:
            if re.match(r'[\-: …!?;\]\[()]', term) == None:
                # print(term)
                # refinement: mutliple matches?
                if term in dict_country_to_geolocation:
                    keyterm = term
                    longitude = dict_country_to_geolocation[term][0]
                    latitude = dict_country_to_geolocation[term][1]
        
        #shoe decided key term
        print("Key term:", keyterm)
        print()

        #for cases don't find key term(s)
        if longitude == '':
            print("No key term for: ", end = " ")
            for t in title_term_list:
                print(t, end = " ")
            print()

            longitude = "72.123"
            latitude = "60.803"

        """slight alter geolocation to preserve all feeds with same geolocation"""
        change_range = 0.1
        change_long = random.random() * change_range
        change_lati = random.random() * change_range

        if random.random() < 0.5:
            long_f = float(longitude) 
            long_f -= change_long
        else:
            long_f = float(longitude) 
            long_f += change_long

        if random.random() < 0.5:
            lati_f = float(latitude) 
            lati_f -= change_lati
        else:
            lati_f = float(latitude) 
            lati_f += change_lati

        longitude = str(long_f)
        latitude = str(lati_f)

        """Write the feed information into csv file"""
        feedwriter.writerow([i + 1] + [val.title] + [val.published] + [val.link]
                                    + [longitude] + [latitude])

        
        
        



