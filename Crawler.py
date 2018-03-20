# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs,re
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		f = open('exporter_help_text.txt', 'r')
		print f.read()
		f.close()

		return

	try:
		opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "lang=", "output="))

		tweetCriteria = got.manager.TweetCriteria()
		outputFileName = "tweets.txt"
		idFileName = "id.txt"

		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg

			elif opt == '--since':
				tweetCriteria.since = arg
				outputFileName += '-'+arg
				idFileName += arg

			elif opt == '--until':
				tweetCriteria.until = arg
				outputFileName += '-'+arg
				idFileName += arg

			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg

			elif opt == '--toptweets':
				tweetCriteria.topTweets = True

			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
			
			elif opt == '--near':
				tweetCriteria.near = '"' + arg + '"'
			
			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--lang':
				tweetCriteria.lang =  arg

			elif opt == '--output':
				outputFileName = arg
				idFileName = 'id-'+arg
		print('output to '+outputFileName)
				
		outputFile = codecs.open(outputFileName, "w+", "utf-8")
		idFile = codecs.open(idFileName, "w+")


		print('Searching...\n')

		def receiveBuffer(tweets):
			for t in tweets:
				outputFile.write(('%s\n' % (t.text)))
				idFile.write(('%s\n' % (t.id)))
			outputFile.flush()
			idFile.flush()
			print('More %d saved on file...\n' % len(tweets))

		def text_processor(text):
			return re.sub(r'@[^\s]*|#[^\s]*', '', text)

		def selector(text):
			return len(text.split()) >= 7

		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer, selector=selector, text_processor=text_processor)

	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
		outputFile.close()
		idFile.close()
		print('Done. Output file generated "%s".' % outputFileName)


if __name__ == '__main__':
	main(sys.argv[1:])
