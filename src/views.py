from flask import Flask, render_template, request , session, redirect, url_for, flash, json, Response
from . models import Models
#from . forms import getDriverForm
from src import app


models = Models()

def transform(RowMapping):
    output = []
    for row in RowMapping:
        output.append(dict(row))
    return output


@app.route('/')
def index():
    return 'main_page__11'  #render_template('index.html')

@app.route('/dates/all', methods=['GET', 'POST'])
def showDates():
    date = models.getAllDates()
    date = transform(date)
    return date #render_template('date.html', date=date)


@app.route('/drivers/all', methods=['GET', 'POST'])
def showDrivers():
    driver = models.getAllDrivers()
    driver = transform(driver)
    return driver #render_template('driver.html', driver=driver)


@app.route('/drivers/search/', methods=['GET', 'POST'])
def getDriverByID():
    if request.method == 'POST':  
        driver_id = request.args.get('driver_id')
        driver = models.getDriverByID(driver_id)
        driver = transform(driver)
        if len(driver) == 0:
            return 'driver not found' #render_template('driver.html', driver=driver)
        return driver #render_template('driver.html', driver=driver)
    else: 
        return 'no method:{}'.format(request.method)

@app.route('/ontimerate/', methods =['GET', 'POST'])
def getAvgOnTimeRate():
    rate = models.getAvgOnTimeRate()
    rate = transform(rate)
    return rate 

@app.route('/totalorders/', methods =['GET', 'POST'])
def getTotalOrders():
    ordercount = models.getTotalOrders()
    ordercount = transform(ordercount)
    return ordercount

@app.route('/totalordervalue/', methods =['GET', 'POST'])
def getTotalOrderValue():
    ordervalue = models.getTotalOrderValue()
    ordervalue = transform(ordervalue)
    return ordervalue

@app.route('/totalpickupdriver/', methods =['GET', 'POST'])
def getTotalPickupDrivers():
    drivercount = models.getTotalPickupDrivers()
    drivercount = transform(drivercount)
    return drivercount

@app.route('/ordersbymonth/', methods =['GET', 'POST'])
def getOrdersPerMonth():
    ordersPerMonth = models.getOrdersPerMonth()
    ordersPerMonth = transform(ordersPerMonth)
    return ordersPerMonth

@app.route('/orderpctbywarehouse/', methods =['GET', 'POST'])
def getOrderPerWarehouse():
    ordersPerW = models.getOrderPerWarehouse()
    ordersPerW = transform(ordersPerW)
    return ordersPerW





if __name__ == '__main__':
    app.run(debug=True)


