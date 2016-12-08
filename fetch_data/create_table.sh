db_path=./test_1.db
echo "drop table history_stock_info; " | sqlite3 $db_path
echo "create table history_stock_info (\
    ID INTEGER PRIMARY KEY AUTOINCREMENT,\
    STOCKNAME TEXT,\
    TODAYOPENPRICE DOUBLE,\
    YESTERDAYCLOSEPRICE DOUBLE,\
    NOWPRICE DOUBLE,\
    TODAYHIGHEST DOUBLE,\
    TODAYLOWEST DOUBLE,\
    BUYPRICE DOUBLE,\
    SELLPRICE DOUBLE,\
    SUCCNUM INT,\
    SUCCPRICE INT,\
    BUYONENUMBER INT,\
    BUYONEPRICE DOUBLE,\
    BUYTWONUMBER INT,\
    BUYTWOPRICE DOUBLE,\
    BUYTHREENUMBER INT,\
    BUYTHREEPRICE DOUBLE,\
    BUYFOURNUMBER INT,\
    BUYFOURPRICE DOUBLE,\
    BUYFIVENUMBER INT,\
    BUYFIVEPRICE DOUBLE,\
    SELLONENUMBER INT,\
    SELLONEPRICE DOUBLE,\
    SELLTWONUMBER INT,\
    SELLTWOPRICE DOUBLE,\
    SELLTHREENUMBER INT,\
    SELLTHREEPRICE DOUBLE,\
    SELLFOURNUMBER INT,\
    SELLFOURPRICE DOUBLE,\
    SELLFIVENUMBER INT,\
    SELLFIVEPRICE DOUBLE,\
    NOWDATE DATE,\
    NOWTIME TIME,\
    INSERTTIME TIME);" | sqlite3 $db_path
