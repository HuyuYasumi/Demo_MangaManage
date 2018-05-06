import os, requests, time, asyncio, aiohttp
from html.parser import HTMLParser
from .header import Header

header = {
    'Cookie': Header.Cookie,
    'User-Agent': Header.User_Agent
}
turl = {}
ftitle = ''
pname = ''

async def imagefile(url, count):
    global pname
    print('downloading:', url)
    target = str(count) + '_' + url.split('/')[-1]
    tmp = os.path.join(pname, target)
    async with aiohttp.ClientSession() as client:
        if os.path.exists(tmp):
            print('existed:', url)
        else:
            async with client.get(url) as f:
                with open(tmp, 'wb') as image:
                    i = await f.read()
                    image.write(i)
            print('downloaded:', target)

def getimage(url, title):
    global pname
    lpath = './images'
    if not os.path.exists(lpath):
        os.mkdir(lpath)
    tname = title
    local_base = 'file:///home/natsu/文档/Demo_YamiboManga/Demo_YamiboManga/images'
    local_link = os.path.join(local_base, tname)
    pname = os.path.join(lpath, tname)
    if not os.path.exists(pname):
        os.mkdir(pname)
    tasks = [imagefile(x, y) for x, y in url.items()]
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    return local_link


class MyHTMLParser(HTMLParser):
    flag, title = False, False
    def handle_starttag(self, tag, attrs):
        global turl
        if tag == 'span':
            for attr in attrs:
                if 'thread_subject' in attr[1]:
                    self.title = True
        if tag == 'td':
            for attr in attrs:
                if 't_f' in attr[1]:
                    self.flag = True
        if self.flag:
            if tag == 'img':
                for cl in attrs:
                    if cl[0] == 'file':
                        print('found image:', cl[1])
                        self.count += 1
                        if 'data/attachment/forum' in cl[1] and not 'yamibo' in cl[1]:
                            turl['https://bbs.yamibo.com/'+cl[1]] = self.count
                        else:
                            turl[cl[1]] = self.count

    def handle_data(self, data):
        global ftitle
        if self.title:
            ftitle = ''.join(c for c in data if c not in r'<>|*"/?:')
            print("\nstart downloading:", ftitle)
            self.count = 0
            self.title = False

    def handle_endtag(self, tag):
        if self.flag and tag == 'td':
            self.flag = False

def main(url):
    if url != '':
        try:
            uhtml = requests.get(url, headers = header, timeout = 10).text
            parser = MyHTMLParser()
            parser.feed(uhtml)
            local_link = getimage(turl, ftitle)
            print('\nEnd.')
            return local_link
        except:
            print("Network Error: " + url)
    else:
        print('bye!')

if __name__ == '__main__':
    url = input('Yamibo\'s url: ')
    main(url)
