## SPARTAN protocol snapshot tool
import tkinter
import requests
import time
import csv
import datetime

listcoinsid=['binancecoin','canyacoin','thorchain','matic-network','cream-2','dos-network','chiliz','sharering','wazirx','harmony',
           'ankr','tixl','unification','concierge-io','contentos','newton-project','waykichain','troy','atomic-wallet-coin',
             'v-id-blockchain','top-network','lto-network','givly-coin','nexo','morpheus-labs','raven-protocol','cubiex', 'cashaa',
             'trust-wallet-token', 'loki-network']
listcoinsname=['binance coin','canya coin','thorchain','matic-network','irisnet','dos-network','chiliz','share token','wazirx','harmony',
           'ankr','tixl','unification','travala','contentos','newton-project','waykichain','troy','atomic-wallet-coin',
              'v-id-blockchain','top-network','lto-network','givly-coin','nexo','morpheus-labs','raven-protocol','cubiex', 'cashaa',
             'trust-wallet-token', 'loki-network']
listcoins = [(listcoinsid[i], listcoinsname[i]) for i in range(0, len(listcoinsid))] 

req_timeout=5

#Check timestamp on https://www.unixtimestamp.com/index.php
startdate=1598443200 # Aug. 26 2020 at 12 PM (noon) UTC
enddate=1599652800 # Sept. 9 2020 at 12 PM (noon) UTC


class App:

    def __init__(self, wind):
        global varGr, mlist, mlist2, keypass
        frame = tkinter.Frame(wind)

        w2 = tkinter.Label(frame, text="TimeStamp start (see https://www.unixtimestamp.com/index.php):")
        w2.pack(side = tkinter.TOP, anchor = tkinter.W)
       
        vcmd = (frame.register(self.callbackE))
        w = tkinter.Entry(frame, validate='all', validatecommand=(vcmd, '%P')) 
        w.insert(0,startdate) 
        w.pack(side = tkinter.TOP, anchor = tkinter.W)

        w2b = tkinter.Label(frame, text="TimeStamp start (see https://www.unixtimestamp.com/index.php):")
        w2b.pack(side = tkinter.TOP, anchor = tkinter.W)
       
        vcmdb = (frame.register(self.callbackEb))
        wb = tkinter.Entry(frame, validate='all', validatecommand=(vcmdb, '%P')) 
        wb.insert(0,enddate) 
        wb.pack(side = tkinter.TOP, anchor = tkinter.W)

        w3 = tkinter.Label(frame, text="Tokens List:")
        w3.pack(side = tkinter.TOP, anchor = tkinter.W)
        mlist2 = tkinter.Listbox(frame, height=16, width=100)
        mlist2.pack(side=tkinter.TOP, fill=tkinter.BOTH)

               
        self.button = tkinter.Button(
                frame, text="QUIT", command=self.quitting
                )
        self.button.pack(side = tkinter.RIGHT)

        self.load = tkinter.Button(
                frame, text="Run (will take up to 30 seconds)", command=run_it
                )
        self.load.pack(side = tkinter.LEFT)

        self.load = tkinter.Button(
                frame, text="Save to CSV file", command=savefile
                )
        self.load.pack(side = tkinter.LEFT)

       
        frame.pack()


    def quitting(self):
        root.destroy()

    def callbackE(self, P):
        global startd
        if str.isdigit(P):
            startd = P 
            return True
        elif P == "":
            startd=startdate
            return True
        else:
            return False

    def callbackEb(self, P):
        global endd
        if str.isdigit(P):
            endd = P 
            return True
        elif P == "":
            endd=enddate
            return True
        else:
            return False
            
                               
root = tkinter.Tk()
root.title("Spartan Snapshot tool V1.0 Sept. 2020")

    
def run_it():
    global prices, startd,endd
    mlist2.insert(0,"--------------------------------------------")
    #Check if it is run before snapshot date
    d = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970,1,1)
    t = (d - epoch).total_seconds()
    if t < enddate:
        mlist2.insert(0,"WARNING, Snapshot date has still not occured!!!!!!")
    else:
        mlist2.insert(0,"SNAPSHOT date has occured, data are valid.")
    nb_days=(float(endd)-float(startd))/3600/24
    prices=[]
    for coin in listcoins:
        try:
            url = ('https://api.coingecko.com/api/v3/coins/%s/market_chart/range?vs_currency=usd&from=%s&to=%s' %(coin[0],startd,endd))
            response = requests.get(url, timeout=req_timeout)
            #print(response)
            r=response.json()
            #print(r)
            sumprices=0
            numprices=0
            temp=[]
            if 'prices' in r:
                for j in range(len(r['prices'])):
                    sumprices=sumprices+float(r['prices'][j][1])
                    numprices=numprices+1
            if numprices != 0:
                mlist2.insert(0,"Average price on " + str(nb_days) +" days of " + coin[1] + " = " + str(sumprices/numprices) + " USD")
                temp.append(coin[1])
                temp.append(sumprices/numprices)
                prices.append(temp)
            else:
                mlist2.insert(0,"UPS! " + coin[1] + " had an issue... no price for it")
            time.sleep(0.5)

        except FileNotFoundError:
            print("Problem while handling token" + coin[1])
    mlist2.insert(0,"--------------------------------------------")
    
def savefile():
    global prices
    with open('SPARTAN_SNAPSHOT.csv', 'w') as file:
        writer = csv.writer(file,lineterminator='\n')
        writer.writerows(prices)

#MAIN CALL

app= App(root)
root.mainloop()




