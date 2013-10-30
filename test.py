import pytumblr
import json
import random
from flask import *

app = Flask(__name__)

@app.route('/top')
def total():
    newlist = sorted(pics.items(), key=lambda x: x[1]) #this is neat
    return render_template("top.html", pics=reversed(newlist))
    
@app.route('/contact')
def contact():
    #do something with this later, probably a github link
    return render_template("contact.html")
    
@app.route('/')
def mash():
    pic1 = random.choice(pics.keys())
    pic2 = random.choice(pics.keys())
    pics[pic1] += 2
    pics[pic2] += 7
    return render_template("hello.html", pic1 = pic1, pic2 = pic2)

credentials = json.loads(open('tumblr_credentials.json', 'r').read())
client = pytumblr.TumblrRestClient(credentials["consumer_key"], credentials["consumer_secret"], credentials["oauth_token"], credentials["oauth_token_secret"])

following = client.following()

#create list of blogs, put in list
blogs = following["blogs"]
tosearch = []
for blog in blogs:
    tosearch.append(blog["url"])

#create dictionary with original picture URLs and set the count to 0
pics = {}
for blog in tosearch:
    resp = client.posts(blog[7:].rstrip('/'), type='photo', tag='me')
    for post in resp["posts"]:
        for orig in post["photos"]:
            pics[orig["original_size"]["url"]] = 0

    
    
#WHY WAS THIS SO HARD    
if __name__ == '__main__':
    app.run(debug=True)    
    
        
