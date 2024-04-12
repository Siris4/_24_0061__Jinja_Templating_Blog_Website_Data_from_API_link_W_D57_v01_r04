from flask import Flask, render_template, url_for
import datetime as dt
import requests

app = Flask(__name__)

# Global list of posts for simplicity; consider a database for production use
posts = [{'id': 1, 'title': 'First Post', 'subtitle': 'Welcome to the first post'},
         {'id': 2, 'title': 'Second Post', 'subtitle': 'Here is the second one'}]

@app.route('/')
def home():
    this_year = dt.datetime.now().year
    MY_NAME = "Gavin"
    return render_template('index.html',
                           CURRENT_YEAR=f'Copyright {this_year} - Built by {MY_NAME}',
                           posts=posts)

all_posts = []

@app.route("/blog/<num>")
def get_blog(num):
    print(f'num is: {num}')
    global all_posts
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    blog_response = requests.get(blog_url)
    blog_response.raise_for_status()
    all_posts = blog_response.json()
    return render_template("post.html", posts=all_posts)  # assuming post.html can handle displaying multiple posts

@app.route('/post/<int:post_id>')
def post(post_id):
    global all_posts
    # finds the post by ID
    post = next((item for item in all_posts if item['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    else:
        return "Post not found", 404


if __name__ == "__main__":
    app.run(debug=True)
