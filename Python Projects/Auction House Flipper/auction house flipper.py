-#This python file uses the hypixel skyblock api to find good deals on the ingame market
maxnum = 1000

# the way the item list works is
# name of item, teir of item, amount of prices, placeholder list of prices, minium discount (in coins)
import requests
import pyperclip as pc
import time
items = {
    '7': ['Juju Shortbow', 'EPIC', 7, [], 2100000],
    '8': ['The Art of War', 'LEGENDARY', 7, [], 750000],
    '9': ['Flower of Truth', 'LEGENDARY', 7, [], 750000],
    '10': ['Spirit Sceptre', 'LEGENDARY', 7, [], 1750000],
    '11': ['Frozen Scythe', 'RARE', 7, [], 1250000],
    '12': ['Axe of the Shredded', 'LEGENDARY', 4, [],5700000 ],
    '13': ['Reaper Mask', 'LEGENDARY', 7, [],1250000],
    '14': ['Personal Compactor 7000', 'LEGENDARY', 7, [],755000],
    '16': ['Yeti Sword', 'LEGENDARY', 5, [],5500000],
    '17': ['Necron\'s Helmet', 'LEGENDARY', 5, [], 1600000],
    '18': ['Necron\'s Chestplate', 'LEGENDARY', 5, [], 1600000],
    '19': ['Necron\'s Leggings', 'LEGENDARY', 5, [], 1600000],
    '20': ['Necron\'s Boots', 'LEGENDARY', 5, [], 1600000],
    '21': ['Storm\'s Helmet', 'LEGENDARY', 5, [], 1150000],
    '22': ['Storm\'s Chwestplate', 'LEGENDARY', 5, [], 1150000],
    '23': ['Storm\'s Leggings', 'LEGENDARY', 5, [], 1150000],
    '24': ['Storm\'s Boots', 'LEGENDARY', 5, [], 1150000],
    '25': ['Wither Chestplate', 'LEGENDARY', 5, [], 1600000],
    '26': ['Wither Leggings', 'LEGENDARY', 5, [], 1200000],
    '27': ['Wither Boots', 'LEGENDARY', 5, [], 540000],

}
foundauctions  = []
itemskey = list(items.keys())
def setprice(itemname, bin, price, tier):
    for x in range(len(itemskey)):
        key = itemskey[x]
        if items[key][0] in itemname:
            if bin == True:
                if tier == items[key][1]:
                    items[key][3].append(price)
                    if (len(items[key][3])) > items[key][2]:
                        items[key][3].sort()
                        items[key][3].pop()
def listtoprice():
   for x in range(len(itemskey)):
        key = itemskey[x]
        amount = len(items[key][3])
        Sum = sum(items[key][3])
        print (items[key])
        items[key][3] = int(round(Sum/amount - items[key][4], -5))
def checkformatch(itemname, bin, price, tier, uuid):
    for x in range(len(itemskey)):
        key = itemskey[x]
        if uuid in foundauctions:
            break
        else:
            if items[key][0] in itemname:
                if price <= items[key][3]:
                    if tier == items[key][1]:   
                        if bin == True:
                            print ('found', items[key][0], 'for', price)
                            pc.copy('/viewauction ' + uuid)
                            foundauctions.append(uuid)
                            time.sleep(2)
            elif 'shaded' in itemname:
                if bin == True:
                    if price <=500000:
                        print ('found a shaded talisman for', price)
                        pc.copy('/viewauction ' + uuid)
                        foundauctions.append(uuid)
                        time.sleep(2)
def checkah():
    page = 0
    data = requests.get('https://api.hypixel.net/skyblock/auctions?', params = {'page': page}).json()
    checknum = 0
    time.sleep(1)
    while True:
        data = requests.get('https://api.hypixel.net/skyblock/auctions?', params = {'page': page}).json()
        for x in range(maxnum):
            uuid =  (data['auctions'][checknum]['uuid'])
            itemname = (data['auctions'][checknum]['item_name'])
            bin = (data['auctions'][checknum]['bin'])
            price = (data['auctions'][checknum]['starting_bid'])
            tier = (data['auctions'][checknum]['tier'])
            checkformatch(itemname, bin, price, tier, uuid)
            checknum += 1
        time.sleep(.55)
        page = page + 1
        checknum = 0
        if page == 7:
            page = 0
def pricesetting():
    data = requests.get('https://api.hypixel.net/skyblock/auctions?', params = {'page': 0}).json()
    maxpage = (data['totalPages'])
    page = 0
    checknum = 0
    while True:
        if page == maxpage - 1:
            listtoprice()
            print (items)
            checkah()
        if checknum == maxnum:
            page = page + 1
            data = requests.get('https://api.hypixel.net/skyblock/auctions?', params = {'page': page}).json()
            checknum = 0
            time.sleep(.55)
        itemname = (data['auctions'][checknum]['item_name'])
        bin = (data['auctions'][checknum]['bin'])
        price = (data['auctions'][checknum]['starting_bid'])
        tier = (data['auctions'][checknum]['tier'])
        setprice(itemname, bin, price, tier)
        checknum += 1
pricesetting()
