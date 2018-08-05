"""
ビジネスロジックモジュール
"""
import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
fig = plt.figure()
font = {"family":"Noto Sans CJK JP"}
plt.rc('font', **font)

from pandas.plotting import scatter_matrix
import pandas as pd
import time
import io
 
 
def create_scatter(data):
    
    data = data.replace(',', '\t').replace(' ', '\t')
    df = pd.read_csv(io.StringIO(data), sep='\t')
    
    # プロットを1つ作成
    ax = fig.add_subplot(111)

    # ラベルをつける
    ax.set_xlabel('so')
    ax.set_ylabel('hr')

    # dfの中身を1つ1つ描画
    for index, row in df.iterrows():
        ax.scatter(row[1],row[2],alpha=0.5)
        ax.annotate(row[0],xy=(row[1],row[2]),size=10)


    
    # ファイル名
    filename = time.strftime('%Y%m%d%H%M%S') + ".png"
 
    # 保存先のパス
    save_path = "./static/result/" + filename
 
    # 表示用URL
    url = "result/" + filename
 

    # 保存処理を行う
    plt.savefig(save_path)
 
    # pltをclose
    plt.close()
 
    return url

def insert(con, title, data, img):
    """ INSERT処理 """
    cur = con.cursor()
    cur.execute('insert into results (title, data, img) values (?, ?, ?)', [title, data, img])
 
    pk = cur.lastrowid
    con.commit()
 
    return pk
