import web
import settings
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = web.database(dbn='sqlite', db='itbook.db3')

def render(params = {}, partial = False):
    global_vars = dict(settings.GLOBAL_PARAMS.items() + params.items())

    if partial:
        return web.template.render('templates/', globals=global_vars)
    else:
        return web.template.render('templates/', base='layout', globals=global_vars)

def book_info_list(page=1):
    try:
        page = int(page)
    except ValueError:
        raise web.seeother('/')
    perpage = 20
    offset = (page - 1) * perpage
    books = db.select('books', what='id, title, description', order='id ASC', limit=perpage, offset=offset)
    bookcount = db.query("SELECT COUNT(*) AS count FROM books")[0]
    pages = bookcount.count / perpage
    if bookcount.count % perpage > 0:
        pages += 1
    if page > pages:
        raise web.seeother('/')
    else:
        return render({'title': settings.SITE_NAME, 'menu': False}).index(books, pages)

def search_result_list(search, page):
    try:
        page = int(page)
    except ValueError:
        raise web.seeother('/result/' + search)
    perpage = 10
    offset = (page - 1) * perpage
    books = db.select('books', what='id, title, description', where="upper(title) like upper($search)", order='id ASC', limit=perpage, offset=offset, vars=dict(search='%'+ search +'%'))
    bookcount = db.query("SELECT COUNT(*) AS count FROM books where upper(title) like upper($search)", vars=dict(search='%'+ search +'%'))[0]
    pages = bookcount.count / perpage
    if bookcount.count % perpage > 0:
        pages += 1
    if page > pages and pages != 0:
        raise web.seeother('/result/' + search)
    else:
        return render({'title': settings.SITE_NAME, 'menu': False}).result(books, pages, search)

def render_book_or_none(id):
    try:
        book = db.select('books', what='*', where="id = $id", vars=locals())[0]
    except IndexError:
        raise web.notfound()
    chapters = db.select('chapters', what='*', order='book_id, weight ASC', where="book_id = $id", vars=locals())
    return render({'title': settings.SITE_NAME + ' - ' + book.title, 'menu': False}).book(book, chapters)

def render_chapter_or_none(book_id, weight):
    try:
        chapter = db.select('chapters', what='id, name, content, book_id', where="book_id = $book_id and weight = $weight", vars=locals())[0]
    except IndexError:
        raise web.notfound()
    book = db.select('books', what='*', where="id = $book_id", vars=locals())[0]
    chaptercount = db.query("SELECT COUNT(*) AS count FROM chapters WHERE book_id = $book_id", vars=locals())[0]
    weight = int(weight)
    if chaptercount == 1:
        previous = 0
        next = 0
    elif chaptercount.count == weight:
        previous = weight - 1
        next = 0
    else:
        previous = weight - 1
        next = weight + 1
    return render({'title': settings.SITE_NAME + ' - ' + book.title, 'menu': True, 'bookid': book.id, 'previous': previous, 'next': next}).chapter(book, chapter)
