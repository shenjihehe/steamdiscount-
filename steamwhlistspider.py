#encoding:utf-8
from bs4 import BeautifulSoup
from time import strftime,sleep
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
appids = []
offs = []
origin_prices = []
discount_prices = []
addrs = []
for info in data.select("#wishlist_items > div"):

    if info.select("div.discount_block.discount_block_inline") == []:
        continue
    else:
        game = str(info.select("div.wishlistRowItem > h4")[0].get_text())
        off = str(info.select("div.discount_pct")[0].get_text())
        origin_price= str(info.select("div.discount_original_price")[0].get_text())
        discount_price = str(info.select("div.discount_final_price")[0].get_text())
        addr = str(info.select("div.storepage_btn_ctn > a")[0].get('href'))
        appid = addr.split("/")[-1]
        print("%s\n\t原价：%s，现价：%s，折扣：%s，商品页面：%s，" % (game, origin_price, discount_price, off, addr))
        appids.append(appid)
        discount_prices.append(discount_price)
        origin_prices.append(origin_price)
        offs.append(off)
        addrs.append(addr)
        result = str(game +"      原价： " +origin_price+"现价： "+discount_price+"折扣： "+off+"商品页面： "+addr)
        fq.write(result+"\n")
print("------------------------------------------------------")
fenge = "-------------------------------------------------------"
fq.write(fenge+"\n")
print("比对分析中，请稍候.....")
message = "分析结果："
fq.write(message+"\n")
for appid,off,origin_price,discount_price,addr in zip(appids,offs,origin_prices,discount_prices,addrs):
    url="https://steamdb.info/app/{}/".format(appid)
    response = requests.get(url)
    data = BeautifulSoup(response.text,"lxml")
    game_name = data.select("td[itemprop='name']")[0].get_text()
    off1 = off[1:]
    off1 = int(off1[:-1])
    a = 75
    b = 80
    c =90
    for wb_data in data.select("#prices > table > tbody > tr"):
        if wb_data.select("td[data-cc='cn']") == []:
            continue
        else:
            s_data = wb_data.select("td:nth-of-type(2)")[0].get_text()
            discount = s_data[-4:]
            lowest_price=s_data[:-7]
            lowest_price1 = float(lowest_price[1:])
            discount1 =discount[1:]
            discount1=int(discount1[:-1])
            print("%s\n原价：%s，现价：%s，折扣：%s，史低：%s，史低折扣：%s，商品页面：%s" %(game_name,origin_price,discount_price,off,lowest_price,discount,addr))
            result = str(game_name + "      原价： " + origin_price + "现价： " + "史低："+lowest_price +discount_price + "折扣： " +off  +"史低折扣："+discount+"商品页面： " + addr)
            fq.write(result + "\n")
            print("购买建议分析中：")
            discount_price = discount_price[1:]
            discount_price = int(discount_price)

            if discount_price > lowest_price1:
                advise = "购买建议:高于史低不推荐购买"
                fq.write(advise+"\n")
                print(advise)
                break
            elif discount_price == lowest_price1:
                advise = "购买建议:已到史低"
                fq.write(advise + "，")
                print(advise)
            else:
                print("低于史低")
                advise = "购买建议:已低于史低"
                fq.write(advise + "，")
                print(advise)

            if  b> off1 >= a:
                advise = "折扣已过75off了，可以入手了！"
                fq.write(advise + "\n")
                print(advise)
            elif c> off1 >=b:
                advise = "折扣已过80off了，值得入手了！"
                fq.write(advise + "\n")
                print(advise)

            elif off1 >=c:
                advise = "折扣已过90off了，快入手吧，难道你还能等到99off?"
                fq.write(advise + "\n")
                print(advise)
            else:
                advise = "未达到75off,可以观望下！"
                fq.write(advise + "\n")
                print(advise)



        sleep(3)
        
fq.write(fenge+"\n")
today = datetime.datetime.now().strftime('%Y-%m-%d')
fq.write("保存时间： "+today+"\n\n\n\n")
fq.close()
print("结果保存在resul.txt中")

os.system("pause")