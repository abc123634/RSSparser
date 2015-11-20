import feedparser
import urllib.parse
import re

"""Prompt for user interest"""
query = input("我想知道關於: ")
query = query.encode('utf8')

# is_topic = input("是否指定主題(Y/N):")
# if is_topic == 'Y' or is_topic == 'y':
# 	topic = input("國際=w 台灣=n 財經=b 科技=t 體育=s 娛樂=e 兩岸=c 社會=y 健康=m: ")
# 	vaild = re.compile(r"[wnbtsecym]")
# 	if vaild.search(topic) is None:
# 		topic = ""


"""Parse chinese characters into url"""
query = urllib.parse.quote(query)

#Google News RSS
url_request = 'https://news.google.com.tw/news?cf=all&hl=zh-TW&pz=1&ned=us&q=' + query + '&output=rss' \
			+ '&tbs=qdr:d,sbd:1' + '&tbm=nws' + 'source=lnt&sa=X' + '&biw=1779&bih=951&dpr=1'

#地球圖輯隊RSS
url_request_yam = 'http://world.yam.com/rss.php'


print(url_request)
# print(repr(query))

# if is_topic == 'Y' or is_topic == 'y':
# 	topic_url = '&topic=' + topic
# 	url_request +=  topic_url



"""Show retrieved seed"""
# f = feedparser.parse(r'test_feed.rss')
# f = feedparser.parse('https://news.google.com.tw/news?cf=all&hl=zh-TW&pz=1&ned=us&q=%22%E5%8F%B0%E7%81%A3%22+OR+%22%E6%B3%95%E5%9C%8B%22&output=rss')
f = feedparser.parse(url_request)

# print(f.feed)

print(f.feed.title + " (" + f.feed.published + ")")


for i, val in enumerate(f.entries):

	# print(val.summary_detail.value)
	print(str(i + 1) + ". " + val.title + "\n"
		+ val.published + "\n"
	    + val.link + "\n")




