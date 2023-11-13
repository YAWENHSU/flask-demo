from flask import Flask
from datetime import datetime

app = Flask(__name__)

# 首頁


@app.route('/')
@app.route('/index')
def index():
    today = datetime.now()
    print(today)
    return f'Hello world!{today}'


@app.route('/books')
def get_all_books():
    books = {1: "Python book", 2: "Java book", 3: "Flask book"}
    return books


@app.route('/books/<int:id>')
def get_books(id):
    try:
        books = {1: "Python book", 2: "Java book", 3: "Flask book"}
        return books[id]
    except Exception as e:
        print(e)
    return '<h1>書籍編號不正確</h1>'


@app.route('/bmi/name=<name>&weight=<w>&height=<h>')
def BMI_Calc(name, w, h):
    bmi = round(eval(w)/(eval(h)/100)**2, 2)
    return {"bmi": bmi}


if __name__ == '__main__':
    app.run(debug=True)
