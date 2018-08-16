from mazeweb import app

@app.route('/')
@app.route('/index')
def index():
        return "Hallo, Lucas!"
