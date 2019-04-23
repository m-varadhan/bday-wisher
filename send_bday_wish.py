#!/usr/bin/env python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEImage import MIMEImage
import PIL

from datetime import datetime
(date, month, year) = (datetime.now().day, datetime.now().month, datetime.now().year)

global sender_cfg, recevr_cfg, subject_fmt
global sender, username, password
global body_msg

def match_bday_babies(date,month):
    with open("bday.csv","r") as br:
        for line in br.readlines():
            #print(line)
            (name,d,m)=line.strip().split("|")
            #print("name:%s:%s:%s: == :%s:%s:\n"%(name,d,m,date,month))
            if (int(d) == int(date)) and (int(month) == int(m)):
                yield name

def select_file_from_dir(dir,cnt):
    import os
    files = os.listdir(dir)
    return files[cnt%len(files)]


def send_bday_email(bbname):
    receivers = recevr_cfg
    subject = subject_fmt.format(name=bbname)
    
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = sender
    msgRoot['To'] = ",".join(receivers)
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msgRoot.attach(msg)
    html = \
    """<html>
    <head><style>
    .bgimg {
        background-image: url("cid:image1");
    }
    </style>
    </head>
    <body> 
    <img src="cid:image1"/>
    </body></html>
    """
    
    htmlpart=MIMEText(html,'html')
    msg.attach(htmlpart)
    
    #image filename used for color and text format
    #0:255:255:255:250:500:.jpg
    #0 - index
    #255:255:255 - RGB
    #250:500 - X,Y of TEXT
    image_dir = "./images"
    #print ("%s:%s:%s:%s"%(date,month,year,((date+month+year)%5)))
    image_file = select_file_from_dir("./images",date+month+year)
    image_fname = '%s/%s'%(image_dir,image_file)
    #print(image_fname)
    #return
    
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw 
    shadowcolor = 128
    
    img = Image.open(image_fname)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("PTS76F.ttf", 40)
    #print(tuple(map(lambda x: int(x), image_fname.split(":")[4:6])))
    draw.text(tuple(map(lambda x: int(x), image_fname.split(":")[4:6])),body_msg%(bbname),
            tuple(map(lambda x: int(x),image_fname.split(":")[1:4])),font=font)
    img.save("/tmp/out.jpg")
    
    fp = open("/tmp/out.jpg", 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)
    #print("attaching the image: %s"%(image_fname))
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.ehlo()
        server.login(username,password)
        server.sendmail(sender, receivers, msgRoot.as_string())         
        server.close()
        print "Successfully sent email"
    except:
        print "Error: unable to send email"

if __name__ == '__main__':
    import yaml

    global sender_cfg, recevr_cfg, subject_fmt
    global sender, username, password

    with open("config.yml") as cfg:
        dmp = yaml.safe_load(cfg) 
    
    return_only_list = lambda a: a if a is None or isinstance(a,list) else [a]
    
    sender_cfg  = dmp["birthday"]["email"]["sender"]
    recevr_cfg  = return_only_list(dmp["birthday"]["email"]["receivers"])
    subject_fmt = dmp["birthday"]["email"]["subject"]
    body_msg    = dmp["birthday"]["email"]["body"]
    
    sender   = sender_cfg["userid"]
    username = sender
    password = sender_cfg["passwd"]

    for babyname in match_bday_babies(date,month):
        send_bday_email(babyname)

