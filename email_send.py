import smtplib
from os.path import splitext, basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

def make_email(me, passw, you, host, port, text=None, subject=None, html=None,image=None, images=None, image_names_in_html=None,
               file_to_add=None):
    msg = MIMEMultipart('alternative')
    if subject is not None:
        msg['subject'] = subject
    else:
        msg['subject'] = "Default"
    msg['From'] = me
    msg['To'] = you
    if text is None and html is None:
        raise Exception("No text and html")
    # data set up
    if text is not None:
        part_text = MIMEText(text, 'plain')
        msg.attach(part_text)
    if html is not None:
        part_html = MIMEText(html, 'html')
        # display images in html file
        if image is not None:
            try:
                fd =open(image, 'rb')
                print(image)
                print(basename(image))
                part_image = MIMEImage(fd.read(), '{}'.format(splitext(basename(image))[0]))
                part_image.add_header('Content-ID', '<{}>'.format(splitext(basename(image))[0]))
                msg.attach(part_image)
                fd.close()
            except Exception:
                print("Error occured")
        if images is not None and image_names_in_html is not None:
            for i, k in zip(images, image_names_in_html):
                try:
                    fd = open(i, 'rb')
                    part_image = MIMEImage(fd.read(), '{}'.format(splitext(basename(i))[0]))
                    part_image.add_header('Content-ID', '<{}>'.format(splitext(basename(i))[0]))
                    msg.attach(part_image)
                    fd.close()
                except Exception:
                    print("Error occured")
        msg.attach(part_html)
    if file_to_add is not None:
        for i in file_to_add:
            try:
                fd = open(i, 'rb')
                part = MIMEApplication(fd.read(), Name=''.format(splitext(basename(i))[0]))  # gets only name
                part['Content-Disposition'] = 'attachment; filename={}'.format(
                    basename(i))  # gets only a file name with ext
                msg.attach(part)
                fd.close()
            except Exception:
                print("Error")

    # sending

    s = smtplib.SMTP_SSL(host, port)
    s.login(me, passw)
    text = msg.as_string()
    s.sendmail(me, you, text)
    s.quit()


if __name__ == '__main__':
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           Кис))<br>
           Ссылка просто тестовая)) <a href="http://www.python.org">link</a> you wanted.
        </p>
        <img src="cid:photo">
      </body>
    </html>
    """
    images = list()
    images.append("/home/strawberry/Downloads/photo.jpeg")

    make_email('', '', '', 'smtp.gmail.com',
               465, text=text, subject="My new letter", html=html, images=images, image_names_in_html=images,
               file_to_add=images)
