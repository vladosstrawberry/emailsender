from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from email_send import make_email



def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return resp.status_code == 200 and content_type is not None and content_type.find('html') > 1


def log_error(error):
    print(error)


def get_wash_post_nav_bar_items():
    response = simple_get("https://www.washingtonpost.com")
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        found_ul = [ul for ul in html.find('ul', attrs={"class":"menu inline-list homepage-nav hidden-xs","id":"sections-menu-wide"})]
        found_a = [i.find('a') for i in found_ul if i != " "]
        # tuple of navigation bar (topic, link)
        result = [(i.text, i['href']) for i in found_a]
        return result
    return None

def download_photo(url):
    data = get(url).content
    path = ((url.split('/')[-1]).split("?")[0]).split("&")[0]
    print(path)
    fd = open(path, "wb")
    fd.write(data)
    fd.close()
    return path

#itemprop="itemListElement" - stories
def get_some_articles(url):
    response = simple_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        desc = [i for i in html.find_all('div', attrs={"itemprop":"itemListElement","itemtype":"http://schema.org/ListItem"})]
        story_b = [i.find("div", attrs={"class": "story-body col-xs-8 col-md-8"}) for i in desc if i.find("div", attrs={"class": "story-body col-xs-8 col-md-8"}) is not None]
        image_b = [i.find("div", attrs={"class": "story-image col-xs-4 col-md-4"}) for i in desc if i.find("div", attrs={"class": "story-image col-xs-4 col-md-4"}) is not None]
        headlines = [(k.text, k['href']) for k in (i.find("a", attrs={"data-pb-local-content-field":"web_headline"}) for i in story_b)]
        image_data = [i.find("img") for i in image_b]
        # (("Text of article", "link to article"), image)
        return headlines, image_data
    return None


def constract(html):
    template_beg = "<html><head></head><body>"
    template_end = "</body></html>"
    images = list()
    for i in html.find_all('img'):
        path = i['data-hi-res-src']
        added = download_photo(str(path))
        images.append(added)
        i.attrs = {}
        i['src'] = "cid:" + added.split(".")[0]
    new_html = (template_beg + html.prettify() + template_end)
    print(new_html)
    return new_html, images


def constract_html(me, password, you, headlines, image_data, max=0):
    #if len(data) < 0 or data is None:
    #    raise Exception("No images")
    template_beg = "<html><head></head><body>"
    template_end = "</body></html>"
    images = list()
    htmls = list()
    for i in image_data:
        path = i['data-low-res-src']
        added = download_photo(str(path))
        images.append(added)
        i['src'] = "cid:" + added.split(".")[0]
    print(str(image_data[1]))
    for i in range(len(headlines)):
        htmls.append(template_beg + str(image_data[i]) + "<p>" + str(headlines[i][0]) + "</p>" + template_end)
    print(htmls)

    for i in range(max):
        html = BeautifulSoup(htmls[i], 'html.parser')
        make_email(me, password, you, "smtp.gmail.com", 465,
                   subject="New letterkk",
                   html=htmls[i], image=images[i])



    # make_email(', '', '', 'smtp.gmail.com',
    #          465, subject="My new letter",)

#написать сервер нужно


if __name__ == '__main__':
    me = "@gmail.com"
    password = "PASS"
    you = "@gmail.com"
    b = get_some_articles('https://www.washingtonpost.com/politics/')
    constract_html(me, password, you, b[0], b[1], 2)
