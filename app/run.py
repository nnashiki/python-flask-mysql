
# ライブラリをインポート
import os
import models
from flask import Flask, render_template, request, redirect, url_for, g


# MySQLドライバはmysql.connector
import MySQLdb
# Dockerを使う場合で、初期設定の場合hostは"192.168.99.100"
# MySQLのユーザやパスワード、データベースはdocker-compose.ymlで設定したもの
connector = MySQLdb.connect(
            user='python',
            passwd='python',
            host='172.18.0.1',
            port=3306,
            db='sample',
            charset='utf8')

connector.ping(True)
cursor = connector.cursor()
cursor.execute("select * from users")

disp = ""
for row in cursor.fetchall():
    disp = "ID:" + str(row[0]) + "  名前:" + row[1]

cursor.close
connector.close

# Flaskはインスタンスを生成する
app = Flask(__name__)
app.config.update({'DEBUG': True })


def connect_db():
    """ データベス接続に接続します """
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con
 
 
def get_db():
    """ connectionを取得します """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
 
 
@app.teardown_appcontext
def close_db(error):
    """ db接続をcloseします """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/hello')
def hello():
    # return "Flask DBから取得 "+disp
    # Jinjaを使う
    title = "ようこそ"
    message = "DBから取得 "+disp
    # index.html をレンダリングする
    return render_template('hello.html', message=message, title=title)

@app.route('/')
def index():
    """ 一覧画面 """
    return render_template('index.html', results={})


@app.route('/create')
def create():
    """ 新規作成画面 """
    return render_template('edit.html')


@app.route('/analysis', methods=['POST'])
def analysis():
    """ 分析実行処理 """
 
    title = request.form['title']
    data = request.form['data']

    img = models.create_scatter(data)
 
    #con = get_db()
 
    #pk = models.insert(con, title, data, img)
    pk = 'true'
    return redirect(url_for('view', pk=pk))


@app.route('/delete/<pk>', methods=['POST'])
def delete(pk):
    """ 結果削除処理 """
    return redirect(url_for('index'))


@app.route('/view/<pk>')
def view(pk):
    """ 結果参照処理 """
    return render_template('view.html', result={'id':'1','title':'データ','img':'result/result.png','data':'aaa aaa aaa'})





if __name__ == '__main__':
    app.run(host='0.0.0.0')
