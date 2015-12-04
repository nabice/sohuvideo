#!/usr/bin/env python

import json
import urllib2
import re
import cookielib
import sys
import subprocess

if len(sys.argv) != 2:
    sys.exit(-1)
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
r = opener.open(sys.argv[1])
data = r.read()
vid = re.search("var vid *=[^0-9]+([0-9]+)", data).group(1)
pid = re.search("(var.*? pid =[^0-9]+|\"pid\":)([0-9]+)", data).group(2)
data = json.loads(opener.open("http://hot.vrs.sohu.com/vrs_flash.action?vid="+vid+"&pid="+pid).read())['data']
fd = open("/tmp/sohu.video.url", "w")
for i in range(len(data['hc'])):
    fd.write("http://data.vod.itc.cn/?new="+data['su'][i]+"&vid="+vid+"&mkey="+data['hc'][i]+"plat=17&prod=h5"+"\n")
fd.close()
subprocess.call("/home/nabice/src/wechat/plugin/3", shell=True)
subprocess.call("mkfifo -m 777 /tmp/mplayer.fifo;DISPLAY=:0 mplayer --playlist=/tmp/sohu.video.url --fs -quiet -slave -input file=/tmp/mplayer.fifo &", shell=True)
