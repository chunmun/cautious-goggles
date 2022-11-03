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

@app.errorhandler(404)
def error404(e):
    return render_template('404.html')


@app.route('/test', methods =['GET', 'POST']) #Calvin: Make dashboard as main page
def test():
    order_value = getTotalOrderValue()
    total_orders = getTotalOrders()
    total_drivers = getTotalPickupDrivers()
    avg_otr = getAvgOnTimeRate()
    otr_per_m = getOntimeRatePerMonth()
    order_per_w = getOrderPerWarehouse()
    
    order_value = str(order_value[0].get('total_order_value'))
    total_orders = str(total_orders[0].get('total_order'))
    total_drivers = str(total_drivers[0].get('total_pickup_driver'))
    avg_otr = avg_otr[0].get('pickup_ontime_rate')
    # otr_per_m = str(otr_per_m[0].get('ontime_rate'))
    # order_per_w = str(order_per_w[0].get('order_pct'))
   
    return render_template('test.html', order_value=order_value
    ,total_orders= total_orders, total_drivers= total_drivers
    ,avg_otr=avg_otr,otr_per_m=otr_per_m, order_per_w= order_per_w)
    #--calvin


@app.route('/', methods =['GET', 'POST']) #Calvin: Make dashboard as main page
def dashboard():
    order_value = getTotalOrderValue()
    total_orders = getTotalOrders()
    total_drivers = getTotalPickupDrivers()
    avg_otr = getAvgOnTimeRate()
    otr_per_m = getOntimeRatePerMonth()
    order_per_w = getOrderPerWarehouse()
    
    order_value = str(order_value[0].get('total_order_value'))
    total_orders = str(total_orders[0].get('total_order'))
    total_drivers = str(total_drivers[0].get('total_pickup_driver'))
    avg_otr = avg_otr[0].get('pickup_ontime_rate')
    # otr_per_m = str(otr_per_m[0].get('ontime_rate'))
    # order_per_w = str(order_per_w[0].get('order_pct'))
   
    return render_template('dashboard.html', order_value=order_value
    ,total_orders= total_orders, total_drivers= total_drivers
    ,avg_otr=avg_otr,otr_per_m=otr_per_m, order_per_w= order_per_w)
    #--calvin

# @app.route('/')
# def index():
#     return render_template('dashboard.html') #render_template('index.html')  #--calvin

@app.route('/packages', methods=['GET', 'POST']) #Calvin: changed from '/packages/all'
def showPackages():
    packages = models.getAllPackages()
    packages = transform(packages)
    return render_template('packages.html', packages=packages) #render_template('showPackages.html', packages=packages) --calvin 

@app.route('/drivers', methods=['GET', 'POST']) 
def showDrivers():
    driver = models.getAllDrivers()
    driver = transform(driver)
    return render_template('drivers.html', driver=driver)

@app.route('/pickups', methods=['GET', 'POST'])
def showPickups():
    pickups = models.getAllPickups()
    pickups = transform(pickups)
    return render_template('pickups.html', pickups=pickups)


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

#@app.route('/ontimerate/', methods =['GET', 'POST'])
def getAvgOnTimeRate():
    rate = models.getAvgOnTimeRate()
    rate = transform(rate)
    return rate 

#@app.route('/totalorders/', methods =['GET', 'POST'])
def getTotalOrders():
    ordercount = models.getTotalOrders()
    ordercount = transform(ordercount)
    return ordercount

#@app.route('/totalordervalue/', methods =['GET', 'POST'])
def getTotalOrderValue():
    ordervalue = models.getTotalOrderValue()
    ordervalue = transform(ordervalue)
    return ordervalue

#@app.route('/totalpickupdriver/', methods =['GET', 'POST'])
def getTotalPickupDrivers():
    drivercount = models.getTotalPickupDrivers()
    drivercount = transform(drivercount)
    return drivercount

#@app.route('/ordersbymonth/', methods =['GET', 'POST'])
def getOrdersPerMonth():
    ordersPerMonth = models.getOrdersPerMonth()
    ordersPerMonth = transform(ordersPerMonth)
    return ordersPerMonth

#@app.route('/orderpctbywarehouse/', methods =['GET', 'POST'])
def getOrderPerWarehouse():
    ordersPerW = models.getOrderPerWarehouse()
    ordersPerW = transform(ordersPerW)
    return ordersPerW

#@app.route('/ontimeratepermonth/', methods =['GET', 'POST'])
def getOntimeRatePerMonth():
    otr = models.getOntimeRatePerMonth()
    otr = transform(otr)
    return otr




if __name__ == '__main__':
    app.run(debug=True)


