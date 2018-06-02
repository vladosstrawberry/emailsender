from scrap import simple_get, constract
from bs4 import BeautifulSoup
from email_send import make_email

def get_article(url):
    response = simple_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        article = html.find('div', attrs={"id": "article-body"})
        image = article.find('img')
        link = image['data-hi-res-src']
        article = article.find('article')
        for tag in article:
            if tag.name == "wp-ad" or tag.name == "script":
                tag.decompose()
            if tag.name == "div":
                image_local = tag.find('img')
                if image_local is not None:
                    tag.replace_with(image_local)
                else:
                    tag.decompose()
        result = constract(article, image)
        return result


if __name__ == '__main__':
    html, images = get_article("https://www.washingtonpost.com/world/national-security/the-us-is-trying-to-find-a-discreet-way-to-pay-for-kim-jong-uns-hotel-in-singapore/2018/06/01/776055ce-9745-439e-9ee4-c0cef8e81523_story.html?utm_term=.3b9a2c86b901")
    make_email('', '', '', 'smtp.gmail.com',
               465, subject="News", html=html, images=images, image_names_in_html=images)
        
