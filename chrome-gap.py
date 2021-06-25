import urllib2
import smtplib
import sys
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

chrome_version_used=sys.argv[1]

def web_scrapping():
    chrome_page = 'https://en.wikipedia.org/wiki/Google_Chrome_version_history'
    page = urllib2.urlopen(chrome_page)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find('table', attrs={'class': 'wikitable sortable'})
    #print name_box
    table_body = name_box.find('tbody')
    #print table_body
    rows = table_body.find_all('td')
    trs = table_body.find_all('tr')
    #print rows
    for tr in trs:
        st = str(tr)
        if "background:#a0e75a" in st:
            data = tr.ul

    for row in rows:
        st = str(row)
        if "background:#a0e75a" in st:
            version = row.contents[0]
#            return version
    return(data,version)


def create_html(chrome_version_used, last_stable_chrome_version, data):
    html = """\
    <html lang='en'>
    <head>
    <title> Regression chrome version Vs Last chrome version </title>
    </head>
    <body>
    <h1> Regression chrome version Vs Last chrome version </h1>
    <table border=2>
    <tr bgcolor='#ffe0b3'><td><b>Chrome version used for regression</b></td>
    <td><b> %s <b></td></tr>
    <tr bgcolor='#a0e75a'><td><b>Latest stable Chrome version</b></td>
    <td><b> %s <b></td></tr>
    </table>
    <br>
    <h2> Significant changes (fixes): </h2>
    %s
    </body>
    </html>
    """
    html = html % (chrome_version_used, last_stable_chrome_version, data)
    Html_file= open(r'/report.html',"w")
    Html_file.write(html)
    Html_file.close()


def send_html(chrome_version_used, last_stable_chrome_version):
    sender = "example@gmail.com"
    receiver = "example@gmail.com"
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Chrome-Gap"
    msg['From'] = sender
    msg['To'] = receiver
    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html lang='en'>
    <head>
    <title> Regression chrome version Vs Last chrome version </title>
    </head>
    <body>
    <h1> Regression chrome version Vs Last chrome version </h1>
    <table border=2>
    <tr bgcolor='#ffe0b3'><td><b>Chrome version used for regression</b></td>
    <td><b> %s <b></td></tr>
    <tr bgcolor='#a0e75a'><td><b>Latest stable Chrome version</b></td>
    <td><b> %s <b></td></tr>
    </table>
    <br>
    </body>
    </html>
    """
    html = html % (chrome_version_used, last_stable_chrome_version)
    # Record the MIME types of both parts - text/plain and text/html.
    part = MIMEText(html, 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part)
    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

(data,last_stable_chrome_version) = web_scrapping()
create_html(chrome_version_used,last_stable_chrome_version,data)
#print last_stable_chrome_version
#send_html(chrome_version_used,last_stable_chrome_version)
