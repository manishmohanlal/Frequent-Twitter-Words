import urllib
import sys
import simplejson
NUMBER_OF_TWEETS = 1000

url= "https://api.twitter.com/1/statuses/user_timeline.json?trim_user=true&count="

def parseTweets(content):
	tweets = list()
	content = simplejson.loads(content)	
	for tweet in content:
		tweets.append(tweet['text'])
	return tweets

def fetchTweet(count,username,page):
	try:
		urlhandler = urllib.urlopen(url+str(count)+"&screen_name="+username+"&page="+str(page))	
		content = urlhandler.read()
		return parseTweets(content)

	except:
		print("Unable to fetch. Trying Again.")
		fetchTweet(count,username,page)		

def getTweets(n,username):
	all_tweets = list()
	page=1
	while n>0:
		if n<200:
			tweets = fetchTweet(n,username,page)
		else:
			tweets = fetchTweet(200,username,page)
		if len(tweets)==0:
			return all_tweets
		all_tweets.extend(tweets)
		page+=1
		n=n-len(tweets)
	return all_tweets

def sortWordsInTweets(total_tweets):
	word_freq = dict()
	for tweet in total_tweets:
		words=tweet.split()
		for word in words:
			if word in word_freq:
				word_freq[word]=word_freq[word]+1
			else:
				word_freq[word]=1
	for word in sorted(word_freq, key=word_freq.get, reverse=True):
		print word.encode('utf-8')

def main():
	total_tweets = getTweets(NUMBER_OF_TWEETS,sys.argv[1])
	sortWordsInTweets(total_tweets)

if __name__=="__main__":
	main()
