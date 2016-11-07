db_path=./trading_record.db
echo "drop table trading_record; " | sqlite3 $db_path
echo "create table trading_record (\
    ID INTEGER PRIMARY KEY AUTOINCREMENT,\
    ORDERID INT,\
    STOCKID TEXT,\
    BUYSELL INT,\
    PRICE DOUBLE,\
    AMOUNT INT,\
    ISSUCCUSS INT,\
    NOWDATE DATE,\
    NOWTIME TIME);" | sqlite3 $db_path
