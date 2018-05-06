import os, requests, time, asyncio, aiohttp
from bs4 import BeautifulSoup
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
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lpath = os.path.join(BASE_DIR, 'images')
    if not os.path.exists(lpath):
        os.mkdir(lpath)
    tname = title
    local_link = os.path.join(BASE_DIR, tname)
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

def getImageUrl(url):
    global turl, ftitle
    try:
        rg  = requests.get(url, headers = header, timeout = 10)
    except:
        print("Network Error: " + url)
        return
    html = BeautifulSoup(rg.text, 'lxml')
    ftitle = ''.join(c for c in html.find('span', id = 'thread_subject').text if c not in r'<>|*"/?:')
    print("\nstart downloading:", ftitle)
    count = 0
    urls = html.find_all('ignore_js_op')
    for u in urls:
        count += 1
        image_url = u.find_all('img')[2].get('file')
        print('found image:', image_url)
        if 'data/attachment/forum' in image_url and not 'yamibo' in image_url:
            turl['https://bbs.yamibo.com/'+image_url] = count
        else:
            turl[image_url] = count
    return turl, ftitle


if __name__ == '__main__':
    url = input('Yamibo\'s url: ')
    if url != '':
        turl_ftitle = getImageUrl(url)
        getimage(turl_ftitle[0], turl_ftitle[1])
        print('\nEnd.')
    else:
        print('bye!')
