import os, requests, time, asyncio, aiohttp
from html.parser import HTMLParser
from .header import Header
from multiprocessing import Pool

header = {
    'Cookie': Header.Cookie,
    'User-Agent': Header.User_Agent
}
turl = {}
ftitle = ''
pname = ''

def imagefile(url, count):
    global pname
    print('downloading:', url)
    target = str(count) + '_' + url.split('/')[-1]
    path = os.path.join(pname, target)
    if os.path.exists(path):
        print('existed:', url)
    else:
        rq = requests.get(url, timeout = 10)
        try:
            image = open(path, 'wb')
            try:
                image.write(rq.content)
            except Exception as e:
                raise e
            finally:
                image.close()
        except Exception as e:
            raise e
        finally:
            rq.close()
        print('downloaded:', target)

def getimage(url_dir, title):
    global pname
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lpath = os.path.join(BASE_DIR, 'images')
    if not os.path.exists(lpath):
        os.mkdir(lpath)
    pname = os.path.join(lpath, title)
    if not os.path.exists(pname):
        os.mkdir(pname)
    local_link = 'file:///' + pname
    p = Pool()
    try:
        for url, count in url_dir.items():
            p.apply_async(imagefile, args=(url, count))
    except Exception as e:
        raise e
    finally:
        p.close()
        p.join()
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
    uhtml = requests.get(url, headers = header, timeout = 10).text
    parser = MyHTMLParser()
    parser.feed(uhtml)
    local_link = getimage(turl, ftitle)
    print('\nEnd.')
    return local_link

if __name__ == '__main__':
    url = input('Yamibo\'s url: ')
    if url != '':
        main(url)
    else:
        print('Url is empty')

