import pytumblr
import json
import random
from flask_oauth import OAuth
from flask import *

app = Flask(__name__)
setupdone = False

app.secret_key = 'people who think they know everything really like lisp'

oauth = OAuth()
credentials = json.loads(open('tumblr_credentials.json', 'r').read())
tumblr = oauth.remote_app('tumblr',
    base_url='api.tumblr.com/v2',
    request_token_url='http://www.tumblr.com/oauth/request_token',
    access_token_url='http://www.tumblr.com/oauth/access_token',
    authorize_url='http://www.tumblr.com/oauth/authorize',
    consumer_key=credentials["consumer_key"],
    consumer_secret=credentials["consumer_secret"]
)

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
    print session
    if 'tumblr_token' not in session:
        return render_template("login.html")
    if not setupdone:
        setup()
    pic1 = random.choice(pics.keys())
    pic2 = random.choice(pics.keys())
    return render_template("hello.html", pic1 = pic1, pic2 = pic2)

def setup():
    # credentials = json.loads(open('tumblr_credentials.json', 'r').read())
    # 
    # consumer = oauth.Consumer(credentials["consumer_key"], credentials["consumer_secret"])
    # client = oauth.Client(consumer)
    # resp, content = client.request(request_token_url, "POST")
    # request_token = dict(urlparse.parse_qsl(content))
    # print request_token
    # #authorize URL time!
    # print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
    # 
    # oauth_verifier = raw_input('Insert oauth_verifier')
    # #sign request?
    # token = oauth.Token(request_token['oauth_token'],
    #     request_token['oauth_token_secret'])
    # token.set_verifier(oauth_verifier)
    # client = oauth.Client(consumer, token)
    # 
    # resp, content = client.request(access_token_url, "POST")
    # access_token = dict(urlparse.parse_qsl(content))
    # #get final tokens?
    # oauth_token = access_token['oauth_token']
    # oauth_token_secret = access_token['oauth_token_secret']

    client = pytumblr.TumblrRestClient(credentials["consumer_key"], credentials["consumer_secret"], session["tumblr_token"][0], session["tumblr_token"][1])

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
    
    
@app.route('/login', methods=['GET','POST'])
def login():
    if session.has_key('tumblr_token'):
        session.pop('tumblr_token', None)
    return tumblr.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))

@app.route('/logout')
def logout():
    print session
    session.pop('tumblr_token', None)
    print session
    setupdone = False
    return redirect(url_for('mash'))
 
#i'm really not entirely sure why i need this, I don't think i do
@tumblr.tokengetter
def get_token():
    return session.get('tumblr_token')

@app.route('/oauth-authorized')
@tumblr.authorized_handler
def oauth_authorized(resp):
    session['tumblr_token'] = (
       resp['oauth_token'],
       resp['oauth_token_secret']
    )
    return redirect(url_for('mash')) 
    
        
if __name__ == '__main__':
    app.run(debug=True)    
    