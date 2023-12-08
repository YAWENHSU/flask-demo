from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
import json

app = Flask(__name__)
books = {1: "Python book", 2: "Java book", 3: "Flask book"}
ascending = True
df = None

# 首頁


@app.route('/')
@app.route('/index')
def index():
    today = get_now()
    print(today)
    return render_template('index.html', today=today)


@app.route('/bmi/name=<name>&weight=<w>&height=<h>')
def BMI_Calc(name, w, h):
    bmi = round(eval(w)/(eval(h)/100)**2, 2)
    return {"bmi": bmi}


@app.route("/books")
def get_all_books():
    books = {
        1: {
            "name": "Python book",
            "price": 299,
            "image_url": "https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348"
        },

        2: {

            "name": "Java book",
            "price": 399,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348"
        },

        3: {
            "name": "C# book",
            "price": 499,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348"
        },
    }

    for id in books:
        print(id, books[id]["name"], books[id]
              ["price"], books[id]["image_url"])
    return render_template("books.html", books=books, today=get_now())


@app.route('/books/<int:id>')
def get_books(id):
    try:
        books = {1: "Python book", 2: "Java book", 3: "Flask book"}
        return books[id]
    except Exception as e:
        print(e)
    return '<h1>書籍編號不正確</h1>'


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@app.route("/pm25-chart")
def pm25_chart():
    return render_template('pm25-chart.html')


@app.route("/county-pm25-json/<county>")
def get_county_pm25_json(county):
    global df
    url = 'https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV'
    pm25 = {}
    try:
        if df is None:
            print(1)
            df = pd.read_csv(url).dropna()
        pm25 = (df.groupby('county').get_group(county)[
            ['site', 'pm25']].set_index('site').to_dict()['pm25'])
        success = True
        message = "資料取得成功!"

    except Exception as e:
        message = str(e)
        success = False

    json_data = {"datetime": get_now(), "success": success, "title": county,
                 "pm25": pm25, "message": message}
    return json.dumps(json_data, ensure_ascii=False)


@app.route("/pm25-json")
def get_pm25_json():
    global df
    six_counties = ['新北市', '臺北市', '桃園市', '臺中市', '臺南市', '高雄市']
    url = 'https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV'
    df = pd.read_csv(url).dropna()

    six_data = {}
    for county in six_counties:
        six_data[county] = round(df.groupby(
            'county').get_group(county)['pm25'].mean(), 2)

    json_data = {
        "title": "PM2.5數據",
        "xData": df["site"].tolist(),
        "yData": df["pm25"].tolist(),
        "sixData": six_data,

    }
    return json.dumps(json_data, ensure_ascii=False)


@app.route("/pm25", methods=["GET", "POST"])
def get_pm25():
    global ascending
    url = 'https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV'
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sort = False
    # 確定回傳方法
    if request.method == "POST":
        if request.form.get('sort'):
            sort = True

    # 製作升降序功能
    try:
        df = pd.read_csv(url).dropna()
        if sort:
            df = df.sort_values("pm25", ascending=ascending)
            ascending = not ascending
        else:
            ascending = True
        columns = df.columns.tolist()
        values = df.values.tolist()

        lowest = df.sort_values('pm25').iloc[0][['site', 'pm25']].values
        highest = df.sort_values('pm25').iloc[-1][['site', 'pm25']].values

        message = "取得資料成功!"
    except Exception as e:
        print(e)
        message = "取得資料失敗，請稍後再試"

    return render_template('pm25.html', **locals())


if __name__ == '__main__':
    app.run(debug=True)
