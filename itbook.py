# -*- coding: utf-8 -*-
import web
import settings
from helpers import *

urls = (
  '/', 'home',
  '/about/', 'about',
  '/page/(.*)', 'index',
  '/book/(.*)', 'book',
  '/chapter/(.*)', 'chapter',
  '/search/', 'search',
  '/result/(.*)', 'result',
  '/sendmail/', 'sendmail')

app = web.application(urls, globals(), autoreload=True)

web.config.smtp_server = 'smtp.qq.com'
web.config.smtp_port = 25
web.config.smtp_username = '593342541@qq.com'
web.config.smtp_password = '120062580'

class about:
    def GET(self):
        return render({'title': settings.SITE_NAME, 'menu': False}).about()

class home:
    def GET(self):
        return book_info_list()

class index:
    def GET(self, page):
        return book_info_list(page)

class book:
    def GET(self, id):
        return render_book_or_none(id)

class chapter:
    def GET(self, id):
        return render_chapter_or_none(id)

class search:
    def POST(self):
        form = web.input()
        return web.redirect("/result/%s" % form.search)

class result:
    def GET(self, args):
        search = ''
        page = 1
        try:
            page = int(args)
        except:
            try:
                search, page = args.split("/")
            except:
                search = args
        return search_result_list(search, page)

class sendmail:
    def POST(self):
        form = web.input()
        msg = "姓名： %s \n\nE-mail： %s \n\n内容: %s \n\nIP： %s \n\n" % (form.name, form.email, form.message, web.ctx.ip)
        web.sendmail('593342541@qq.com', [settings.RECIP], form.subject, msg, headers={'Content-Type': 'text/plan;charset=utf-8'})
        return 'success'

if __name__ == "__main__":
    app.run()
