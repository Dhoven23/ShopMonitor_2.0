from flask import Flask, render_template, url_for
from Data.mongo_setup import global_init
from Data import Students, key
import Service.admin_svc as asv
global_init('DHoven','12345')



app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    students = Students.Student.objects(Is_signedIn = True)
    keys = key.Key.objects()
    return render_template('home.html', students=students, keys = keys)


@app.route("/about")
def about():
    return "<h1>About Page</h1>"


if __name__ == '__main__':
    app.run(debug=True)