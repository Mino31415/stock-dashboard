import yfinance as yf
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#get all data required
def stockdata(name):

    #iniiate a few variables
    higher = 0 #how many times close > open

    dev0 = 0 #how many times deviation <1%
    dev1 = 0 #how many times 1% <= deviation < 2%
    dev2 = 0 #how many times 2% <= deviation < 3%
    dev3 = 0 #how many times deviation > 3%

    incr0 = 0 #how many times increase < 1%
    incr1 = 0 #how many times 1% < increase < 2%
    incr2 = 0 #how many times 2% < increase < 3%
    incr3 = 0 #how many times increase > 3%

    decl0 = 0 #how many times decline < 1%
    decl1 = 0 #how many times 1% < decline < 2%
    decl2 = 0 #how many times 2% < decline < 3%
    decl3 = 0 #how many times decline > 3%

    changelist = [] #list to store change

      
    stock = yf.Ticker(name) #get stock data
    hist = stock.history(period="1y") #specify timeframe


    open = hist["Open"] #opening price
    close = hist["Close"] #closing price
    high = hist["High"] #peak price
    low = hist["Low"] #lowest price


    x = 0
    while x < len(open)-1: #while loop

        #get data for each day
        temp_open = open[x]
        temp_close = close[x]
        temp_high = high[x]
        temp_low = low[x]


        #get deviation
        deviation = (1-(temp_low / temp_high)) / 2
        #handle deviation
        if deviation < 0.01: #if deviation < 1%
            dev0 += 1
        elif deviation < 0.02: #if <2%
            dev1 += 1
        elif deviation <0.03: #if <3%
            dev2 += 1
        else: #if >3%
            dev3 += 1

        #get increase / decline of stockprice
        change = 1 - temp_open / temp_close
        changelist.append(change*100) #put change in changelist
        if change > 0: #if increase
            if change < 0.01: #if increase < 1%
                incr0 += 1
            elif change < 0.02: #if increase < 2%
                incr1 += 1
            elif change < 0.03: #if increase < 3 %
                incr2 += 1
            else: #if increase > 3%
                incr3 += 1
            higher+=1

        else: #if decline
            if abs(change) < 0.01: #if decline < 1 %
                decl0 += 1
            elif abs(change) < 0.02: #if decline < 2%
                decl1 +=1
            elif abs(change) < 0.03: #if  decline < 3%
                decl2 += 1
            else: #if decline > 3%
                decl3 += 1


        #+1 to get to the next element
        x+=1


    return ((higher/(x+1)), 1-(higher/(x+1))), (incr0, incr1, incr2, incr3), (decl0, decl1, decl2, decl3), (dev0, dev1, dev2, dev3), open, changelist

stock = input("Stock symbol: ")
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"])

higher_lower, increase, decline, deviation, price, pricechange = stockdata(stock)

#Bar diagram
fig1, ax1 = plt.subplots()
height = [100*higher_lower[0] / (higher_lower[0] + higher_lower[1]), 100*higher_lower[1] /  (higher_lower[0] + higher_lower[1])]
labels = ["Percenage of positive days", "Percenatge of negative days"]
ax1.bar(labels, height)
ax1.set_title("Share of increase / decline")

#graph
fig2, ax2 = plt.subplots()
ax2.plot(price)
ax2.set_title("Stock graph")

#pie chart decline
fig3, ax3 = plt.subplots()
total_decline = decline[0] + decline[1] + decline[2] + decline[3]
labels = ['<1%', '<2%', '<3%', '>3%']
sizes = [round(100*decline[0] / total_decline), round(100*decline[1] / total_decline), round(100*decline[2] / total_decline), round(100*decline[3] / total_decline)]
ax3.pie(sizes, labels=labels, autopct='%1.1f%%')
ax3.set_title("Decline on declining days")

#pie chart increase
fig4, ax4 = plt.subplots()
total_increase = increase[0] + increase[1] + increase[2] + increase[3]
labels = ['<1%', '<2%', '<3%', '>3%']
sizes = [round(100*increase[0] / total_increase), round(100*increase[1] / total_increase), round(100*increase[2] / total_increase), round(100*increase[3] / total_increase)]
ax4.pie(sizes, labels=labels, autopct='%1.1f%%')
ax4.set_title("Increase on increasing days")

#horizontal bar chart (deviation)
fig5, ax5 = plt.subplots()
total_days = decline[0] + decline[1] + decline[2] + decline[3] + increase[0] + increase[1] + increase[2] + increase[3]
labels = ['<1%', '<2%', '<3%', '>3%']
width = [round(100*deviation[0] / total_days), round(100*deviation[1] / total_days), round(100*deviation[2] / total_days), round(100*deviation[3] / total_days)]
ax5.barh(labels, width)
ax5.set_title("Total daily deviation around average value")


#Create GUI
root = tk.Tk()
root.title("Stock Dashboard")
root.state('zoomed')


#create frame for first few graphs
frame_top = tk.Frame(root)
frame_top.pack(fill="both", expand=True)

#first figure
canvas1 = FigureCanvasTkAgg(fig1, frame_top)
canvas1.draw()
canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

#second figure
canvas2 = FigureCanvasTkAgg(fig2, frame_top)
canvas2.draw()
canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)


#create lower frame
frame_bottom = tk.Frame(root)
frame_bottom.pack(fill="both", expand=True)

#third figure
canvas3 = FigureCanvasTkAgg(fig3, frame_bottom)
canvas3.draw()
canvas3.get_tk_widget().pack(side="left", fill="both", expand=True)

#fourth figure
canvas4 = FigureCanvasTkAgg(fig5, frame_bottom)
canvas4.draw()
canvas4.get_tk_widget().pack(side="left", fill="both", expand=True)

#fifth figure
canvas5 = FigureCanvasTkAgg(fig4, frame_bottom)
canvas5.draw()
canvas5.get_tk_widget().pack(side="left", fill="both", expand=True)

root.mainloop()