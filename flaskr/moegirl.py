import urllib.request

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

if __name__ == '__main__':
    target_url = 'https://zh.moegirl.org.cn/%E6%97%A5%E6%9C%AC2021%E5%B9%B4%E5%86%AC%E5%AD%A3%E5%8A%A8%E7%94%BB'
    html = url_open(target_url).decode('utf-8')
    f = open("out.html", "w", encoding='utf-8')  
    print(html, file=f)