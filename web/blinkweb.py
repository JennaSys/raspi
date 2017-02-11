import web

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:        
    def GET(self, name):
        params = web.input()
        
        if not name: 
            name = 'world'
        return 'Hello, ' + name + '!\n' + params['x']

if __name__ == "__main__":
    app.run()
