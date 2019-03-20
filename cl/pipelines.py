# -*- coding: utf-8 -*-
import cl.items as items
from json2html import json2html
from datetime import datetime
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail
from cl.settings import MAIL_PASS, MAIL_TO, MAIL_FROM

#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ClPipeline(object):
  sg = sendgrid.SendGridAPIClient(apikey=MAIL_PASS)
  from_email = Email(MAIL_FROM)
  to_email = Email(MAIL_TO)

  def process_item(self, item: items.CarItem, spider):
    self.items.append(item)
    return item

  def open_spider(self, spider):
    self.items = []

  def close_spider(self, spider):
    s = json2html.convert(json=self.items)
    with open("table.tmp.html", "w+") as tablef:
      tablef.write(s)
    subject = "Craiglist Car Search {0}".format(datetime.today().strftime("%x"))
    content = Content("text/html", s)
    mail = Mail(self.from_email, subject, self.to_email, content)
    resp = self.sg.client.mail.send.post(request_body=mail.get())
    print("TOTAL ITEM COUNT = ", len(self.items), "email sent: ",
          resp.status_code)
