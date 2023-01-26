# this code is meant to be used to find "flips", or good deals on items that can be resold for profit later on in the minecraft server hypixel
import requests
import pyperclip as pc
import time
from playsound import playsound
#this was made about last year, so I wasnt very adept with programming at the time, as seen by this dict that could of easily been an array full of nested arrays
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
#this function and listtoprice will set the price of the items im looking for, using an equation that is about ITEM PRICE = Sum of the most cheap -  a certain value configured for each item
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
#this is the code that would be running 99% of the time, it takes all the parameters from the hypixel skyblock api and uses the price set above to find if the item is worth buying
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
                            #shaded was a rare part of a talisman where if it had shaded you could get 1,000,000 from a buyback program of sorts
            elif 'shaded' in itemname:
                if bin == True:
                    if price <=500000:
                        print ('found a shaded talisman for', price)
                        pc.copy('/viewauction ' + uuid)
                        foundauctions.append(uuid)
                        time.sleep(2)
#this function is the one that will pass the data into the checkformatch function above, and you can also see the link to the api in this one
def checkah():
    page = 0
    data = requests.get('https://api.hypixel.net/skyblock/auctions?', params = {'page': page}).json()
    checknum = 0
    time.sleep(1)
    while True:
        data = requests.get('https://api.hypixel.net/skyblock/auctions?', params = {'page': page}).json()
        for x in range(1000):
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
#this function basically runs all of the other functions
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
        if checknum == 1000:
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
