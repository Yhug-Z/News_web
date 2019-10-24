# -*- coding:utf-8 -*-
 ######################################################
#        > File Name: flask_client.py
#      > Author: GuoXiaoNao
 #     > Mail: 250919354@qq.com 
 #     > Created Time: Mon 20 May 2019 11:52:00 AM CST
 ######################################################

from flask import Flask, send_file

app = Flask(__name__)


@app.route('/<username>/favorite')
def topics(username):
    #个人收藏夹列表
    return send_file('templates/favorite.html')

@app.route('/<username>/favorite/<title>/<title_id>')
def topics_detail(username,title, title_id):
    #
    return send_file('templates/favorite_news.html')


if __name__ == '__main__':
    app.run(debug=True)

