import os

from flask import Flask, session, render_template, request, redirect, url_for, send_from_directory
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_socketio import *

app = Flask(__name__)
app.secret_key = 'howsyourday'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
socketio = SocketIO(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#homepage
@app.route("/")
def index():
    if 'loggedin' in session:
        return redirect(url_for('user'))
    return render_template("welcome.html")

#resgistering
@app.route("/signup")
def signup():
    return render_template("signup.html")

#signing up
@app.route("/register", methods=["POST"])
def register():
#storing the information
       username = request.form.get("username")
       firstname = request.form.get("firstname")
       lastname = request.form.get("lastname")
       email = request.form.get("email")
       secure = request.form.get("password")
       pwd = generate_password_hash(secure)
       if db.execute("SELECT * FROM users WHERE username= :username", {"username":username}).rowcount >= 1:
          return render_template("error.html", message="UserName exist")
       db.execute("INSERT INTO users (username,firstname, lastname, email, password) VALUES (:username,:firstname, :lastname, :email, :secure)",
               {"username": username,"firstname": firstname, "lastname": lastname, "email": email, "secure": pwd})
       db.commit()
       return render_template("login.html")

#login route
@app.route("/signin")
def signin():
    return render_template("login.html")

#signing in
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    access = request.form.get("password")
    auth = db.execute("SELECT * FROM users WHERE username= :uname", {"uname": username}).fetchone()
    assume = check_password_hash(auth.password, access)
    if (assume == True):
       session['loggedin'] = True
       session['username'] = request.form['username']
       return redirect(url_for('user'))
    return render_template('error.html', message='check your credentials')

#profile route
@app.route('/user', methods=['GET', 'POST'])
def user():
    if not 'loggedin' in session:
        return redirect(url_for('signin'))
    username = session['username']
    if request.method == 'POST':
        profile = request.files['profile']
        sfname = 'static/'+str(secure_filename(profile.filename))
        profile.save(sfname)
        db.execute("UPDATE users SET profile_pic = :profile WHERE username= :uname", {"uname": username, "profile": profile.filename})
        db.commit()
    user = db.execute("SELECT * FROM users WHERE username= :uname", {"uname": username}).fetchone()
    return render_template('user.html', nameofuser=username, fname=user.firstname, lname=user.lastname, email=user.email, pic=user.profile_pic)

#posts page
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if not 'loggedin' in session:
        return redirect(url_for('signin'))
    if request.method == 'POST':
       com_user = session['username']
       post_id = request.form.get("post-id")
       com_text = request.form.get("comments")
       db.execute("INSERT INTO comments (username, post_id, comment) VALUES (:username,:post_id, :comment)",
               {"username": com_user,"post_id": post_id, "comment": com_text})
       db.commit()
       return post(post_id)
    posts = db.execute("SELECT id, username, post, post_image FROM posts ORDER BY id DESC").fetchall()
    return render_template("posts.html", posts=posts)

#specific post
@app.route('/posts/<int:id>', methods=['GET'])
def post(id):
    if not 'loggedin' in session:
        return redirect(url_for('signin'))
    post = db.execute("SELECT username, post, post_image FROM posts WHERE id = :pid", {"pid": id}).fetchone()
    comment = db.execute("SELECT id, username, comment FROM comments WHERE post_id = :pid", {"pid": id}).fetchall()
    return render_template("post.html",id= id, loggeduser=session['username'], user=post.username, post=post.post, image=post.post_image, comments=comment)

#writing a post and comment
@app.route('/write', methods=['GET', 'POST'])
def write():
    if not 'loggedin' in session:
        return redirect(url_for('signin'))
    username = session['username']
    if request.method == 'POST':
        post = request.form.get("post")
        posted = "True"
        postpic = request.files['postpic']
        sfname = 'static/images/'+str(secure_filename(postpic.filename))
        postpic.save(sfname)
        postimage = postpic.filename
        db.execute("INSERT INTO posts (username, post, post_image, posted) VALUES (:username,:post, :postimage, :posted)",
                {"username": username,"post": post, "postimage": postimage, "posted": posted})
        db.commit()
        return redirect(url_for('posts'))
    return render_template("write.html")

#deleting a comment
@app.route('/delete/<int:pid>/comment/<int:id>', methods=["GET"])
def delcomment(pid, id):
    if not 'loggedin' in session:
        return redirect(url_for('signin'))
    db.execute("DELETE FROM comments WHERE id = :pid", {"pid": id})
    db.commit()
    return redirect(url_for('post', id=pid))

#deleting a post
@app.route('/delete/<int:id>', methods=["GET"])
def delpost(id):
    if not 'loggedin' in session:
        return redirect(url_for('signin'))
    db.execute("DELETE FROM posts WHERE id= :pid", {"pid": id})
    db.commit()
    return redirect(url_for('posts'))

#chat route
@app.route("/chat")
def chat():
    if not 'loggedin' in session:
        return redirect(url_for('signin'))
    message = db.execute("SELECT * FROM globalchat")
    return render_template("chat.html", message=message, msguser=session['username'])

#real time chat and adding messages into database
@socketio.on('message')
def message(data):
    uname = session.get('username')
    msg = data["msg"]
    db.execute("INSERT INTO globalchat (username, message) VALUES (:username, :message)", {"username": uname, "message": msg})
    db.commit()
    emit('roommsg',{'user': uname, 'msg':msg}, broadcast=True)

#deleting message
@app.route('/delmsg/<int:id>', methods=["GET"])
def delmsg(id):
    if not 'loggedin' in session:
        return redirect(url_for('signin'))
    db.execute("DELETE FROM globalchat WHERE id= :pid", {"pid": id})
    db.commit()
    return redirect(url_for('chat'))

#logging out
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return signin()

if __name__ == '__main__':
    socketio.run(app, debug=True)
