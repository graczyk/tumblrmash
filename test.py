import pytumblr
import json
import random
import oauth2 as oauth
import urlparse
from flask import *

request_token_url = 'http://www.tumblr.com/oauth/request_token'
authorize_url = 'http://www.tumblr.com/oauth/authorize'
access_token_url = 'http://www.tumblr.com/oauth/access_token'

app = Flask(__name__)
setupdone = False

@app.route('/top')
def total():
    newlist = sorted(pics.items(), key=lambda x: x[1]) #this is neat
    return render_template("top.html", pics=reversed(newlist))
    
@app.route('/contact')
def contact():
    #do something with this later, probably a github link
    return render_template("contact.html")
    
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        pics[request.form["action"]] += 1
    return mash()
    
@app.route('/')
def mash():
    if not setupdone:
        setup()
    pic1 = random.choice(pics.keys())
    pic2 = random.choice(pics.keys())
    return render_template("hello.html", pic1 = pic1, pic2 = pic2)


def setup():
    credentials = json.loads(open('tumblr_credentials.json', 'r').read())

    consumer = oauth.Consumer(credentials["consumer_key"], credentials["consumer_secret"])
    client = oauth.Client(consumer)
    resp, content = client.request(request_token_url, "POST")
    request_token = dict(urlparse.parse_qsl(content))
    print request_token
    #authorize URL time!
    print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])

    oauth_verifier = raw_input('Insert oauth_verifier')
    #http://www.tumblr.com/oauth/todo.us?oauth_token=NpIuSQeS7ylqQLE9myDXbo97zHwQCW2lCxp15mw8FvmDjZoJqr&oauth_verifier=fze5EExWh54b9Ocv0FdbHXEos1HrxHriV6bsfp175iCioyClyg#_=_
    #sign request?
    token = oauth.Token(request_token['oauth_token'],
        request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))
    #get final tokens?
    print "    - oauth_token        = %s" % access_token['oauth_token']
    print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']

    oauth_token = access_token['oauth_token']
    oauth_token_secret = access_token['oauth_token_secret']

    client = pytumblr.TumblrRestClient(credentials["consumer_key"], credentials["consumer_secret"], oauth_token, oauth_token_secret)

    following = client.following()

    #create list of blogs, put in list
    blogs = following["blogs"]
    tosearch = []
    for blog in blogs:
        tosearch.append(blog["url"])

    #create dictionary with original picture URLs and set the count to 0
    global pics
    pics = {}
    for blog in tosearch:
        resp = client.posts(blog[7:].rstrip('/'), type='photo', tag='me')
        for post in resp["posts"]:
            for orig in post["photos"]:
                pics[orig["original_size"]["url"]] = 0
    global setupdone
    setupdone = True
    
    
#WHY WAS THIS SO HARD    
if __name__ == '__main__':
    app.run(debug=True)    
    
        
