import streamlit as st
import requests
import xml.etree.ElementTree as et
import sqlitecloud
from datetime import datetime


def trendgetir(ulke="TR"):
    r = requests.get(f'https://trends.google.com/trending/rss?geo={ulke}')
    kod = r.status_code
    if kod == 200:
        veri = r.content
        veri = et.fromstring(veri)
        trendler = []
        for i in veri.findall('channel/item'):
            title = i[0].text
            trafik = int(i[1].text.replace("+", ""))
            haberler = []
            for etiket in i:
                if "news_item" in etiket.tag:
                    newsitem = {}
                    newsitem['title'] = etiket[0].text
                    newsitem['url'] = etiket[2].text
                    newsitem['resim'] = etiket[3].text
                    newsitem['kaynak'] = etiket[4].text
                    haberler.append(newsitem)
            trend = {}
            trend['title'] = title
            trend['trafik'] = trafik
            trend['haberler'] = haberler
            trendler.append(trend)

        return trendler
    else:
        return False


def trendekle(title, trafik):
    conn = sqlitecloud.connect(
        "sqlitecloud://cwcgjb0ahz.g1.sqlite.cloud:8860/chinook.sqlite?apikey=DaG8uyqMPa9GdxoR7ObMoajHIdfUOrc7B0mF0IrU6Y0")
    c = conn.cursor()

    c.execute("SELECT rowid,* FROM trendler WHERE title=?", (title,))
    say = c.fetchall()
    if len(say) == 0:
        simdi = str(datetime.now())
        c.execute("INSERT INTO trendler VALUES(?,?,?)", (title, trafik, simdi))
        id = c.lastrowid
        conn.commit()
        return id
    else:
        trend = say
        return trend[0][0]


def haberekle(trend, title, url, resim, kaynak):
    conn = sqlitecloud.connect(
        "ssqlitecloud://cqfo1b00nk.g4.sqlite.cloud:8860/chinook.sqlite?apikey=xc0SwmsxIcqlW6ssoTiJ7z0EzfknKIUI11h1tMPZKGQ")
    c = conn.cursor()

    c.execute("SELECT * FROM haberler WHERE url=?", (url,))
    say = c.fetchall()
    if len(say) == 0:
        simdi = datetime.now()
        tarih = datetime.timestamp(simdi)
        c.execute("INSERT INTO haberler VALUES(?,?,?,?,?,?)", (trend, title, url, resim, kaynak, tarih))
        conn.commit()
        return True

    return False


conn = sqlitecloud.connect(
    "sqlitecloud://cqfo1b00nk.g4.sqlite.cloud:8860/chinook.sqlite?apikey=xc0SwmsxIcqlW6ssoTiJ7z0EzfknKIUI11h1tMPZKGQ")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS trendler(title TEXT,trafik INTEGER,tarih TEXT)")
conn.commit()

c.execute("CREATE TABLE IF NOT EXISTS haberler(trend INTEGER,title TEXT,url TEXT,resim TEXT,kaynak TEXT,tarih INTEGER)")
conn.commit()

c.execute("SELECT trend,titl.kaynak.title FROM haberler ORDER BY rould DESC LIMIT100")
sonuc=c.fetchall()

st.datefrom(sonuc)
