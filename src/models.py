from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os

class Models:
    def __init__(self):
        self.engine = create_engine(os.environ.get('DB_URL', 'postgresql://postgres:Zgjxjayw629@localhost:5432/test_starapp'))
    def executeRawSql(self, statement, params={}):
        out = None
        with self.engine.connect() as con:
            out = con.execute(text(statement), params)
        return out

    def getAllDates(self):
        return self.executeRawSql("SELECT * FROM date_dim;").mappings().all() 
        
    def getAllDrivers(self):
        return self.executeRawSql("SELECT * FROM driver_dim;").mappings().all() #what does mappings().all do?
    
    def getDriverByID(self, id):
        values = self.executeRawSql("""SELECT * FROM driver_dim WHERE driver_key=:id;""", {"id": id}).mappings().all()
        return values 
    
    def getAvgOnTimeRate (self):
        return self.executeRawSql("""select round(count(distinct case when (on_time_counter ='1' or early_counter = '1') then pick_up_order_key else null end) * 1.0/ count(distinct pick_up_order_key ),2 )as pickup_ontime_rate
from pickup_fact;""").mappings().all() 

    def getTotalOrders(self):
        return self.executeRawSql("""select count(distinct pick_up_order_key)  as total_order
from pickup_fact;""").mappings().all() 

    def getTotalOrderValue(self):
        return self.executeRawSql("""select sum(ordervalue) as total_order_value
from pickup_fact;""").mappings().all() 

    def getTotalPickupDrivers(self):
        return self.executeRawSql("""select count(distinct driver_key) as total_pickup_driver
from pickup_fact;""").mappings().all() 

    def getOrdersPerMonth(self):
        return self.executeRawSql("""select dd.month, count(distinct pick_up_order_key) as order_count
    from pickup_fact f left join date_dim dd 
    on f.pickup_date_key = dd.date_key
    where dd.year = 2022
    group by dd.month;""").mappings().all() 

    def getOrderPerWarehouse (self):
        return self.executeRawSql("""select f.warehouse_key, w.name as warehouse_name, ROUND(count(distinct f.pick_up_order_key) *1.0/(select count(distinct pick_up_order_key) from pickup_fact),2) as order_pct
from pickup_fact f left join warehouse_dim w 
on f.warehouse_key = w.warehouse_key 
group by f.warehouse_key, w.name;""").mappings().all() 

    def createModels(self):
            self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS pickup_fact(
                package_key	varchar	,
                warehouse_key	varchar	,
                pick_up_point_key	varchar	,
                driver_key	varchar	,
                late_counter	varchar	,
                early_counter	varchar	,
                on_time_counter	varchar	,
                one_day_late_counter	varchar	,
                two_day_late_counter	varchar	,
                three_day_late_counter	varchar	,
                ordervalue	int	,
                orderweight	float	,
                pick_up_order_key	varchar	,
                service_level_key	varchar	,
                ex_date_key	varchar	,
                pickup_date_key	varchar	,
                pickup_time_key	varchar	,
                ex_time_key	varchar	,
                PRIMARY KEY(pick_up_order_key)
                );
            """)

            self.executeRawSql(
            """create table IF NOT EXISTS date_dim(
                date_key	varchar	,
                dayofweek	int	,
                day	int	,
                month	int	,
                year	int	,
                weekend	int	,
                PRIMARY KEY (date_key));
            """)

            self.executeRawSql(
                """create table IF NOT EXISTS driver_dim(
                    driver_key	varchar	,
                driver_name	varchar	,
                vehicle_type	varchar	,
                    PRIMARY KEY(driver_key)
                );

                """)

            self.executeRawSql(
                """create table IF NOT EXISTS package_dim (
                    package_key	varchar	,
                    length	float	,
                    width	float	,
                    height	float	,
                    size	varchar	,
                    PRIMARY KEY(package_key));
                """)
            self.executeRawSql(
                """create table IF NOT EXISTS pickup_point_dim(
                    pick_up_point_key	varchar	,
                    seller_name	varchar	,
                    postal_code	varchar	,
                    location	varchar	,
                    PRIMARY KEY(pick_up_point_key));
                """)
            self.executeRawSql(
                """create table IF NOT EXISTS service_level_dim (
                service_level_key	varchar	,
                service_level	varchar	,
                PRIMARY KEY(service_level_key));
                """)
            self.executeRawSql(
                """create table IF NOT EXISTS time_dim (
                time_key	varchar	,
                hour	int	,
                minute	int	,
                session	varchar	,
                    PRIMARY KEY(time_key)
                );
                """)
            self.executeRawSql(
                """create table IF NOT EXISTS warehouse_dim(
                warehouse_key	varchar	,
                name	varchar	,
                location	varchar,
                PRIMARY KEY(warehouse_key));
                """)
