from article import get_article
from email_send import make_email
from wash import get_wash_post_nav_bar_items, get_some_articles
import time


def cheduler(youremail, passwd, recepient):
    run = True
    while run:
        cd = get_wash_post_nav_bar_items()
        headlines, htmls_not_used = get_some_articles(cd[0][1])
        for i in range(3):
            print(headlines[i][1])
            html, images = get_article(headlines[i][1])
            make_email(youremail, passwd, recepient, 'smtp.gmail.com',
                       465, subject="News", html=html, images=images, image_names_in_html=images)
        time.sleep(60*60*24)


if __name__ == "__main__":
    me = "@gmail.com"
    password = "PASS"
    you = "@gmail.com"
    cheduler("", "", "")
