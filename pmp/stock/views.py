from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock, Meeting
from django.contrib.auth.decorators import login_required


# Create your views here.

#Can specifiy stocks = 
def createContext(stocks=None):
    stocks = list(Stock.objects.all().exclude(name="Fund Totals").exclude(name="Cash"))
    totals = Stock.objects.get(name="Fund Totals")
    cash = Stock.objects.get(name="Cash")
    securities = {
        'mktVal': totals.mktVal-cash.mktVal,
        'perfToday': (totals.mktVal-cash.mktVal)/(totals.prevClose-cash.mktVal)-1,
        'perfTodayFormatted': ''
    }

    if securities['perfToday'] > 0:
        securities['perfTodayFormatted'] = "+" + str(round(securities['perfToday'] * 100,2)) + "%"
    else:
        securities['perfTodayFormatted'] = str(round(securities['perfToday'] * 100,2)) + "%"
    context = {
        'stocks': stocks,
        'totals': totals,
        'cash': cash,
        'securities': securities,
        'securityVal': securities['mktVal'],
        'securityPerf': securities['perfTodayFormatted'],
        #Splitting securities up like this made Apache work.
    }
    return context

@login_required
def portfolio(request):
    context=createContext()
    return render(request, 'stock/tableHome.html', context)

def about(request):
    return render(request, 'stock/about.html',{'title': 'About'})

def home(request):
    return render(request, 'stock/home.html')

@login_required
def sortedTable(request):
    sortKey=request.GET.get('key')
    sortDirs = request.session.get('sortDirs')

    #TODO: implement date sorting
    if sortDirs is None:
        sortDirs = {
            "direc": True,
            "prevKey": ""
        }
    else:
        sortDirs["direc"] = not sortDirs["direc"]
    
    direction = sortDirs["direc"] and sortDirs["prevKey"]==sortKey
    sortDirs['direc'] = direction

    context = createContext()


    #context['stocks'].sort(key=lambda stock: getattr(stock,sortKey), reverse=(not direction) )
    context['stocks'] = sorted(context['stocks'],key=lambda stock: getattr(stock,sortKey), reverse=(not direction) )

    sortDirs["prevKey"] = sortKey
    request.session['sortDirs'] = sortDirs

    #render automatically looks in templates directory
    return render(request, 'stock/tableHome.html', context)

def demo(request):
    context=createContext()
    return render(request, 'stock/tableHome.html', context)

@login_required
def schedule(request):

    meets = list(Meeting.objects.all())

    stocks = list(Stock.objects.all().exclude(name="Fund Totals").exclude(name="Cash"))

    stocks.sort(key=lambda stock: abs(stock.perfToday), reverse=True)

    movers = stocks[:5]


    context={
        'title': "Presentation Schedule",
        'schedule': meets,
        'movers': movers,
    }
    return render(request, 'stock/schedule.html',context)



