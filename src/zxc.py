from ctypes import addressof
from genericpath import exists
from pickle import TRUE
from sqlite3 import dbapi2
from flask import Flask, render_template, request
import requests

import psycopg2

conn = psycopg2.connect(database="nftdb", user = "postgres", password = "32201510", host = "127.0.0.1", port = "5433")

conn.autocommit = True

cur = conn.cursor()

zxc = Flask(__name__)

@zxc.route('/')
def hello():
    return render_template("hello.html")

@zxc.route('/', methods=['POST'])
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





