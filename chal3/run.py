import string
import urllib2
from bottle import route, run, post, get, request

@get('/')
def index():
    with open(__file__) as f:
        return '<pre>' + "".join({'<':'&lt;','>':'&gt;'}.get(c,c) for c in f.read()) + '</pre>'


@post('/isup')
@get('/isup')
def isup():
    try:
        name = request.params.get('name', None)
        is_remote = request.environ.get('REMOTE_ADDR') != '127.0.0.1'
        is_valid = all(x in name for x in ['http', 'kuchenblech'])
        if is_remote and not is_valid:
            raise Exception
        result = urllib2.urlopen(name).read()
        return result
    except:
        return 'Error'

run(host='0.0.0.0', server="paste", port=8080, reloader=False)
