import urllib,urllib2,json,re,datetime,sys,cookielib
from .. import models
from pyquery import PyQuery

class TweetManager:
	
	def __init__(self):
		pass
		
	# The modified version will remove url automatically from tweets
	@staticmethod
	def getTweets(tweetCriteria, receiveBuffer=None, bufferLength=1000, proxy=None, selector=None, text_processor=None):
		refreshCursor = ''
	
		results = []
		num_collected = 0
		resultsAux = []
		cookieJar = cookielib.CookieJar()
		
		if hasattr(tweetCriteria, 'username') and (tweetCriteria.username.startswith("\'") or tweetCriteria.username.startswith("\"")) and (tweetCriteria.username.endswith("\'") or tweetCriteria.username.endswith("\"")):
			tweetCriteria.username = tweetCriteria.username[1:-1]

		active = True
		num_of_errors = 0

		while active:
			try:
				json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy)
				num_of_errors = 0
			except:
				num_of_errors += 1
				if num_of_errors >= 5:
					print("More than 5 errors are continously received, break")
					break
				continue
			if len(json['items_html'].strip()) == 0:
				break

			refreshCursor = json['min_position']
			scrapedTweets = PyQuery(json['items_html'])
			#Remove incomplete tweets withheld by Twitter Guidelines
			scrapedTweets.remove('div.withheld-tweet')
			tweets = scrapedTweets('div.js-stream-tweet')
			
			if len(tweets) == 0:
				break
			
			for tweetHTML in tweets:
				tweetPQ = PyQuery(tweetHTML)
				tweet = models.Tweet()
				try:
					tweet_text = filter(lambda x: isinstance(x, basestring), tweetPQ("p.js-tweet-text").contents())[0].strip()
				except:
					print("Unable to parse this tweet")
					continue
				txt = re.sub(r"\s+", " ", tweet_text.replace('# ', '#').replace('@ ', '@'))
				id = tweetPQ.attr("data-tweet-id")
				# usernameTweet = tweetPQ("span:first.username.u-dir b").text()
				# retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
				# favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
				# dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
				# permalink = tweetPQ.attr("data-permalink-path")
				
				# geo = ''
				# geoSpan = tweetPQ('span.Tweet-geo')
				# if len(geoSpan) > 0:
				# 	geo = geoSpan.attr('title')
				
				if text_processor:
					txt = text_processor(txt)

				tweet.id = id
				tweet.text = txt
				# tweet.permalink = 'https://twitter.com' + permalink
				# tweet.username = usernameTweet
				# tweet.date = datetime.datetime.fromtimestamp(dateSec)
				# tweet.retweets = retweets
				# tweet.favorites = favorites
				# tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
				# tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
				# tweet.geo = geo
				if selector:
					if selector(txt):
						# results.append(tweet)
						resultsAux.append(tweet)
						num_collected += 1
				else:
					num_collected += 1
					resultsAux.append(tweet)
				
				if receiveBuffer and len(resultsAux) >= bufferLength:
					print(num_collected, "collected,",)
					receiveBuffer(resultsAux)
					resultsAux = []
				
				if tweetCriteria.maxTweets > 0 and num_collected >= tweetCriteria.maxTweets:
					active = False
					break
					
		
		if receiveBuffer and len(resultsAux) > 0:
			receiveBuffer(resultsAux)
		
		# return results
	
	@staticmethod
	def getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy):
		url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"
		
		urlGetData = ''
		
		if hasattr(tweetCriteria, 'username'):
			urlGetData += ' from:' + tweetCriteria.username
		
		if hasattr(tweetCriteria, 'querySearch'):
			urlGetData += ' ' + tweetCriteria.querySearch
		
		if hasattr(tweetCriteria, 'near'):
			urlGetData += "&near:" + tweetCriteria.near + " within:" + tweetCriteria.within
		
		if hasattr(tweetCriteria, 'since'):
			urlGetData += ' since:' + tweetCriteria.since
			
		if hasattr(tweetCriteria, 'until'):
			urlGetData += ' until:' + tweetCriteria.until

		if hasattr(tweetCriteria, 'lang'):
			url += '&l=' + tweetCriteria.lang

		if hasattr(tweetCriteria, 'topTweets'):
			if tweetCriteria.topTweets:
				url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"
		
		
		
		url = url % (urllib.quote(urlGetData), refreshCursor)

		headers = [
			('Host', "twitter.com"),
			('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
			('Accept', "application/json, text/javascript, */*; q=0.01"),
			('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
			('X-Requested-With', "XMLHttpRequest"),
			('Referer', url),
			('Connection', "keep-alive")
		]

		if proxy:
			opener = urllib2.build_opener(urllib2.ProxyHandler({'http': proxy, 'https': proxy}), urllib2.HTTPCookieProcessor(cookieJar))
		else:
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		opener.addheaders = headers

		try:
			response = opener.open(url)
			jsonResponse = response.read()
		except Exception as e:
			print "Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd" % urllib.quote(urlGetData)
			raise
		
		dataJson = json.loads(jsonResponse)
		
		return dataJson		
