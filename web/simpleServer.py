import web

render = web.template.render('templates/')
urls = ('/index', 'index',
        '/add', 'add'
)
app = web.application(urls,globals())

class index:
    def GET(self, param=None):
        # call /templates/index.html
        return render.index(param)
class add:
    def POST(self):
        inputMessage = web.input()
        print "get post" + str(inputMessage)
        return render.success()



if __name__ == "__main__": 
    app.run()
