import email
from enum import unique
from genericpath import exists
from pickle import TRUE
from sqlite3 import dbapi2
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import psycopg2
import psycopg2.extras
import re
from werkzeug.security import generate_password_hash, check_password_hash

conn = psycopg2.connect(database="nftdb", user = "postgres", password = "32201510", host = "127.0.0.1", port = "5433")

conn = psycopg2.connect(database="users", user = "postgres", password = "32201510", host = "127.0.0.1", port = "5433")


conn.autocommit = True

cur = conn.cursor()

zxc = Flask(__name__)
zxc.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
Bootstrap(zxc)


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min = 3, max = 10)])
    password = PasswordField('password', validators=[InputRequired(), Length(min = 6, max = 80)])

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message = 'Invalid email') , Length(max = 40)])
    username = StringField('username', validators=[InputRequired(), Length(min = 3, max = 10)])
    password = PasswordField('password', validators=[InputRequired(), Length(min = 6, max = 80)])

@zxc.route('/')
def mainpg():
    return render_template("mainpg.html")

@zxc.route('/log', methods = ['GET', 'POST'])
def log():
    form = LoginForm()

    if form.validate_on_submit():
        cur.execute("SELECT USERNAME, PASSWORD FROM USERS WHERE username = '"+form.username.data+"' AND password = '"+form.password.data+"'")
        if cur.fetchone() is None:
            return render_template("fail.html")
        else:
            return render_template('hello.html')

    return render_template("log.html", form = form)


@zxc.route('/sign', methods = ['GET', 'POST'])
def sign():
    form = RegisterForm()

    if form.validate_on_submit():
        #hashed_password = generate_password_hash(form.password.data, method='sha256')
        cur.execute(
            "INSERT INTO USERS (USERNAME,PASSWORD, EMAIL) VALUES ('"+form.username.data+"', '"+form.password.data+"', '"+form.email.data+"')"
        )

        return render_template("congrats.html")

    return render_template("sign.html", form = form)



@zxc.route('/hello', methods=['POST'])
def end():
    nft_address = request.form['text']
    cur.execute("SELECT ADDRESS FROM NFT WHERE address = '"+nft_address+"'")
    if cur.fetchone() is None:
        url = f"https://solana-gateway.moralis.io/nft/mainnet/{nft_address}/metadata"
        headers = {
            "accept": "application/json",
            "X-API-Key": "26KEoSTSZ0fDRS3r1izBX5XKqSTkav35AcLquftEPp990rpKjCfEbm2OeCJuPFk9"
        } 
        response = requests.get(url, headers=headers)

        cur.execute(
            "INSERT INTO NFT (URL,INFO, ADDRESS) VALUES ('"+url+"', '"+response.text+"','"+nft_address+"')"
        )
        return render_template('upss.html')
    else:
        cur.execute("SELECT INFO FROM NFT WHERE address = '"+nft_address+"'")
        ans = cur.fetchone()
        info = ans[0]
        cur.execute("SELECT URL FROM NFT WHERE address = '"+nft_address+"'")
        ans = cur.fetchone()
        url = ans[0]
    return render_template('end.html', address = nft_address, info = info, url = url)


if __name__ == "__main__":
    zxc.run(debug=True)





