from django.db import models
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Create your models here.


class Stock(models.Model):
    #FOR FIELDS: USE SECOND HALF OF maker.py OUTPUT

    name=models.TextField(default="")
    ticker=models.TextField(default="")
    avgCost=models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    price=models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    prevClose=models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    perfToday=models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    mktVal=models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    totalCost=models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    shares=models.IntegerField(default=0)
    dates=models.TextField(default="")
    prices=models.TextField(default="")
    history=models.TextField(default="")
    eps=models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    pe=models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    pctGain = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    gain = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    pctGainFormatted=models.TextField(default="")
    perfTodayFormatted=models.TextField(default="")

    #Old Names
    '''ticker = models.TextField()
    price = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    name = models.TextField()
    shares = models.IntegerField()
    avgCost = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    totalCost = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    # add trade date
    mktVal = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    gain = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    pctGain = models.DecimalField(
        max_digits=1000, decimal_places=4, default=0.00)'''


    def save(self, *args, **kawargs):
        super().save(*args, **kawargs)

    def __str__(self):
        return self.ticker+":"+str(self.price)        
    
    #add EPS and PE

class Meeting(models.Model):
    date=models.TextField(default="")
    pres1=models.TextField(default="")
    pres2=models.TextField(default="")
    pres3=models.TextField(default="")
    link1=models.TextField(default="#")
    link2=models.TextField(default="#")
    link3=models.TextField(default="#")
    pop1 = models.BooleanField(default=False)
    pop2 = models.BooleanField(default=False)
    pop3 = models.BooleanField(default=False)


    def save(self, *args, **kawargs):
        super().save(*args, **kawargs)

    def __str__(self):
        return self.date+" - "+self.pres1+": " + self.link1+" / " + self.pres2+": " + self.link2+" / " + self.pres3+": " + self.link3

class StockManager(models.Manager):
    def refresh(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "/etc/config.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("PMP Portfolio").get_worksheet(0)
        sheet.update('A2','Fund Totals') # This line shouldn't be necessary, but updating the sheet makes sure stock prices are live
        data = sheet.get_all_records()

        liszt = list(data)
        # Very crude. TODO: Optimize this when you have time.
        for stock in Stock.objects.all():
            for item in liszt:
                if item["Symbol"] == stock.ticker:
                    if stock.name == "Fund Totals":
                        stock.mktVal = item["Market Value"]
                        stock.prevClose = item['Prev. Market Value']
                        stock.perfToday = stock.mktVal/stock.prevClose-1

                    else:
                        stock.price = item["Last Price ($)"]
                        stock.prevClose = item["Prev. Close"]
                        stock.mktVal = item["Market Value"]
                        stock.eps = item["EPS"]
                        stock.pe = item["P/E"]
                        stock.gain = stock.mktVal-float(stock.totalCost)
                        stock.pctGain = stock.gain/float(stock.totalCost)
                        stock.perfToday = float(stock.price/float(stock.prevClose)-1)
                        if stock.pctGain > 0:
                            stock.pctGainFormatted = "+" + str(round(stock.pctGain * 100,2)) + "%"
                        else:
                            stock.pctGainFormatted = str(round(stock.pctGain * 100,2)) + "%"
                        
                    if stock.perfToday > 0:
                        stock.perfTodayFormatted = "+" + str(round(stock.perfToday * 100,2)) + "%"
                    else:
                        stock.perfTodayFormatted = str(round(stock.perfToday * 100,2)) + "%"
                    stock.save()
                        
                    print(stock.ticker, stock.price, stock.mktVal, round(stock.perfToday,4), stock.perfTodayFormatted)
    
    def updateSchedule(self):
        Meeting.objects.all().delete()
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "/etc/config.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("PMP Portfolio").get_worksheet(2)
        data = sheet.get_all_records(2)

        liszt = list(data)

        for week in liszt:
            meet = Meeting.objects.create(date=week['Date'],pres1=week['pres1'],pres2=week['pres2'],pres3=week['pres3'],link1=week['link1'],link2=week['link2'],link3=week['link3'])
            if meet.link1 != "#":
                meet.pop1 = True
            if meet.link2 != "#":
                meet.pop2 = True
            if meet.link3 != "#":
                meet.pop3 = True
            meet.save()
            print(meet)

    def update(self):
        Stock.objects.all().delete()
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "/etc/config.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("PMP Portfolio").get_worksheet(0)
        sheet.update('A2','Fund Totals') # This line shouldn't be necessary, but updating the sheet makes sure stock prices are live

        data = sheet.get_all_records()

        liszt = list(data)
        for pmpstock in liszt:
            if pmpstock["Description"] == "Fund Totals":
                #PREV CLOSE IS DIFFERENT HERE: REPRESENTS TOTAL MKT VALUE YESTERDAY
                stok = Stock.objects.create(name=pmpstock["Description"],mktVal=pmpstock["Market Value"],id=0,prevClose=pmpstock["Prev. Market Value"])
                stok.perfToday = stok.mktVal/stok.prevClose-1
                if stok.perfToday > 0:
                    stok.perfTodayFormatted = "+" + str(round(stok.perfToday * 100,2)) + "%"
                else:
                    stok.perfTodayFormatted = str(round(stok.perfToday * 100,2)) + "%"
                stok.save()
                print(stok.ticker,stok.price,stok.perfTodayFormatted,sep="\t")


            elif pmpstock["Description"] == "Cash":
                #Quick fix for share count, possibly change at some point
                stok = Stock.objects.create(name=pmpstock["Description"],ticker=pmpstock["Symbol"],avgCost=pmpstock["Cost Basis"],price=pmpstock["Last Price ($)"],prevClose=pmpstock["Prev. Close"],mktVal=pmpstock["Market Value"],totalCost=pmpstock["Original Cost"],shares=round(float(pmpstock["Shares"])+0.5),dates=pmpstock["Trade Date(s)"],prices=pmpstock["Purchase Price(s)"],history=pmpstock["Acquisition History"],eps=pmpstock["EPS"],pe=pmpstock["P/E"])
                continue
            else:
                #INSIDE CREATE: USE FIRST HALF OF maker.py OUTPUT
                stok = Stock.objects.create(name=pmpstock["Description"],ticker=pmpstock["Symbol"],avgCost=pmpstock["Cost Basis"],price=pmpstock["Last Price ($)"],prevClose=pmpstock["Prev. Close"],mktVal=pmpstock["Market Value"],totalCost=pmpstock["Original Cost"],shares=pmpstock["Shares"],dates=pmpstock["Trade Date(s)"],prices=pmpstock["Purchase Price(s)"],history=pmpstock["Acquisition History"],eps=pmpstock["EPS"],pe=pmpstock["P/E"])
                stok.gain = stok.mktVal-stok.totalCost
                stok.pctGain = stok.gain/stok.totalCost
                stok.perfToday = stok.price/stok.prevClose-1
                
                if stok.perfToday > 0:
                    stok.perfTodayFormatted = "+" + str(round(stok.perfToday * 100,2)) + "%"
                else:
                    stok.perfTodayFormatted = str(round(stok.perfToday * 100,2)) + "%"

                if stok.pctGain > 0:
                    stok.pctGainFormatted = "+" + str(round(stok.pctGain * 100,2)) + "%"
                else:
                    stok.pctGainFormatted = str(round(stok.pctGain * 100,2)) + "%"

                stok.save()
                print(stok.ticker,stok.price,stok.perfTodayFormatted,sep="\t")
