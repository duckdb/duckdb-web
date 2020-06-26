import re
import sys

if (sys.version_info > (3, 0)):
	import urllib.request
	fun = urllib.request.urlopen
else:
	import urllib2
	fun = urllib2.urlopen

htmlstring =  fun(sys.argv[1]).read().decode('utf8')
re1 = re.compile(sys.argv[2])
print(re1.search(htmlstring).group(1).strip())