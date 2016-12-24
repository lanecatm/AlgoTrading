use algotradingDB;
drop table if exists outside_pool_record;
create table outside_pool_record (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    TRADINGID INT NOT NULL,
    STOCKID INT, 
    TIME DATETIME, 
    BUYSELL INT, 
    ISSYNC BOOL,
    TRADINGTYPE INT,
    EXPECTAMOUNT INT, 
    EXPECTPRICE DOUBLE,
    ISSUCCESS BOOL, 
    SUCCAMOUNT INT,
    SUCCMONEY DOUBLE,
    SUCCPRICE DOUBLE
);

