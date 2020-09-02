from flask import Flask
from Data.mongo_setup import global_init
import Service.admin_svc as asv
global_init('DHoven','12345')



app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    messages = str()
    message = asv.whos_in_the_shop()
    for mess in message:
        messages = messages + mess + '<br>'
    return f"<h1>{messages}</h1>"


@app.route("/about")
def about():
    return "<h1>About Page</h1>"


if __name__ == '__main__':
    app.run(debug=True)