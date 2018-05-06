import os, requests, asyncio, aiohttp
from bs4 import BeautifulSoup
from .header import Header
from multiprocessing import Pool

header = {
    'Cookie': Header.Cookie,
    'User-Agent': Header.User_Agent
}
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
            p.apply_async(imagefile, args = (url, count))
    except Exception as e:
        raise e
    finally:
        p.close()
        p.join()
    return local_link

def getImageUrl(url):
    rg  = requests.get(url, headers = header, timeout = 10)
    html = BeautifulSoup(rg.text, 'lxml')
    title = ''.join(c for c in html.find('span', id = 'thread_subject').text if c not in r'<>|*"/?:')
    print("\nstart downloading:", title)
    count = 0
    urls = html.find_all('ignore_js_op')
    url_dir = {}
    for u in urls:
        count += 1
        image_url = u.find_all('img')[2].get('file')
        print('found image:', image_url)
        if 'data/attachment/forum' in image_url and not 'yamibo' in image_url:
            url_dir['https://bbs.yamibo.com/'+image_url] = count
        else:
            url_dir[image_url] = count
    return getimage(url_dir, title)


if __name__ == '__main__':
    url = input('Yamibo\'s url: ')
    if url != '':
        getImageUrl(url)
        print('\nEnd.')
    else:
        print('Url is empty!')

