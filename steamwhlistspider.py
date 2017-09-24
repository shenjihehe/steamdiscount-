#encoding:utf-8
from bs4 import BeautifulSoup
from time import strftime
import requests
import os
import sys
import datetime



if not os.path.exists("steam.txt"):
    fp = open("steam.txt","w+")
    fp.close()

file_object = open('steam.txt')
steamId = file_object.read()
if steamId =="":
    print("请在result.txt写入steamid，再重启程序")
    os.system("pause")


url='http://steamcommunity.com/id/{}/wishlist'.format(steamId)
response = requests.get(url)
data = BeautifulSoup(response.text,"lxml")

fq = open("result.txt", 'w+',encoding='utf-8')
for info in data.select("#wishlist_items > div"):

    if info.select("div.discount_block.discount_block_inline") == []:
        continue
    else:
        game = str(info.select("div.wishlistRowItem > h4")[0].get_text())
        off = str(info.select("div.discount_pct")[0].get_text())
        origin_price= str(info.select("div.discount_original_price")[0].get_text())
        discount_price = str(info.select("div.discount_final_price")[0].get_text())
        addr = str(info.select("div.storepage_btn_ctn > a")[0].get('href'))
        print("%s\n\t原价：%s，现价：%s，折扣：%s，商品页面：%s，" % (game, origin_price, discount_price, off, addr))
        result = str(game +"      原价： " +origin_price+"现价： "+discount_price+"折扣： "+off+"商品页面： "+addr)
        fq.write(result+"\n")

today = datetime.datetime.now().strftime('%Y-%m-%d')
fq.write("保存时间： "+today+"\n\n\n\n")
fq.close()
print("结果保存在resul.txt中")

os.system("pause")