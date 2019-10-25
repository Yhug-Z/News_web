# -*- coding:utf-8 -*-
######################################################
#        > File Name: flask_client.py
#      > Author: GuoXiaoNao
#     > Mail: 250919354@qq.com
#     > Created Time: Mon 20 May 2019 11:52:00 AM CST
######################################################

from flask import Flask, send_file

app = Flask(__name__)


@app.route('/index')
def index():
    # 首页
    return send_file('templates/index.html')


@app.route('/politics')
def politics():
    # 国际新闻
    return send_file('templates/politics.html')


@app.route('/foreign')
def foreign():
    # 国外新闻
    return send_file('templates/foreign.html')


@app.route('/finance')
def finance():
    # 财经新闻
    return send_file('templates/finance.html')


@app.route('/tec')
def tec():
    # 科技新闻
    return send_file('templates/tec.html')


@app.route('/sport')
def sport():
    # 体育新闻
    return send_file('templates/sport.html')


@app.route('/ent')
def ent():
    # 娱乐新闻
    return send_file('templates/ent.html')


@app.route('/<news_id>')
def article(news_id):
    # 具体新闻页面
    return send_file('templates/arti176.47.10.229cle.html')


@app.route('/login')
def login():
    # 登录
    return send_file('templates/login.html')


@app.route('/register')
def register():
    # 注册
    return send_file('templates/register.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
