#!/usr/bin/env python
# coding: utf-8
from bs4 import BeautifulSoup
import os
import re
import sys
import urllib.request
import yaml


def main():
    url = 'http://weekly.ascii.jp/comic/kareto/'
    domain = 'http://weekly.ascii.jp'
    dirpath = os.path.abspath(os.path.dirname(__file__))
    y = yaml.load(open(dirpath + '/conf.yaml').read())

    res = urllib.request.urlopen(url)
    date = res.getheader('date')
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    li = soup.find('ul', class_='toplist').find_all('li')
    first_link = li[0].find('a')['href']

    try:
        f = open(dirpath + '/latest.txt', 'r')
        latest_link = f.read().strip()
        f.close()
    except IOError:
        latest_link = ''

    if first_link == latest_link:
        sys.exit()

    atom = '''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<title>彼とカレット。</title>
<link href="http://weekly.ascii.jp/comic/kareto/"/>
<author>
<name>tugeneko</name>
</author>
<id>http://weekly.ascii.jp/comic/kareto/</id>
'''

    atom += '<updated>{0}</updated>\n'.format(date)

    p = re.compile('[0-9]+')

    for item in li:
        h2 = item.find('h2').find('a').string
        link = domain + item.find('a')['href']
        img = domain + item.find('img')['src']
        span = item.find('span').string

        m = p.search(h2)
        if m is None:
            continue

        atom += '<entry>\n'
        atom += '<title>%s</title>\n' % h2
        atom += '<link rel="alternate" type="text/html" href="%s" />\n' % link
        atom += '<id>cullet%s</id>\n' % h2
        atom += '<summary type="text">%s</summary>\n' % span
        atom += '<content type="text/html"><p>%s</p><img src="%s" /></content>\n' % (span, img)
        atom += '<updated>{0}</updated>\n'.format(date)
        atom += '</entry>\n'
    atom += '</feed>'

    f = open(dirpath + '/latest.txt', 'w')
    f.write(first_link)
    f.close()

    try:
        f = open(y['save_path'] + '/cullet.atom', 'w')
        f.write(atom)
        f.close()
        print('complete!')

    except IOError:
        print('error')
        print('cannot open iofile', file=sys.stderr)


if __name__ == "__main__":
    main()
