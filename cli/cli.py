# ==============================================================================
# Filename: cli.py
# Author: Yi Wei
# E-mail: weiyi1994@sjtu.edu.cn
# Description: CLI for this system
# Prerequisite: Click (Installation: 'sudo pip install click', Ref: http://click.pocoo.org/)
# ==============================================================================

import click
import sys
sys.path.insert(0, '../common/')
sys.path.insert(0, '../algo_trading')
from clientOrder import clientOrder
import algo_trading
from datetime import datetime
import sqlite3



dbfile = 'test_0.1.db'


@click.group()
def cli():
	pass

@click.command()
def initdb():
	"""Initialize Database before placing any order."""
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	# Create Table Orders
	cursor.execute('create table orders (id integer primary key autoincrement, buysell text, stockid text, start text, end text, amount int, alg text, status int, total float, ap float, wap float)')
	# cursor.execute('create table results (order id )')
	cursor.close()
	conn.commit()
	conn.close()

@click.command()
@click.option('--buysell', type=click.Choice(['buy','sell']), default='buy', help='Buy or sell the stock? Default is buy')
@click.option('--stockid', prompt=True, help='The ID of the stock you want to trade')
@click.option('--start', prompt=True, help='Start date of executing the order, in Y-m-d')
@click.option('--starttime', help='Start time of executing the order, in H:M:S')
@click.option('--end', prompt=True, help='Start date of executing the order, in Y-m-d')
@click.option('--endtime', help='End time of executing the order, in H:M:S')
@click.option('--amount', prompt=True, help='Number of shares')
@click.option('--alg', type=click.Choice(['twap','vwap']), prompt=True, help='Trading algorithms, TWAP/VWAP')
@click.confirmation_option(help='Are you sure to place this order?')
def placeorder(buysell, stockid, start, starttime, end, endtime, amount, alg):
	"""Place an order"""
	click.echo('Placing Order...')
	# transfer time format
	if starttime is None:
		starttime = '9:00:00'
	if endtime is None:
		endtime = '15:00:00'
	start_t = datetime.strptime(start+' '+starttime, '%Y-%m-%d %H:%M:%S')
	end_t = datetime.strptime(end+' '+endtime, '%Y-%m-%d %H:%M:%S')

	# store into database
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor() 
	cursor.execute(r'insert into orders (buysell, stockid, start, end, amount, alg, status) values (?,?,?,?,?,?,0)',(buysell, stockid, str(start_t), str(end_t), str(amount), alg))
	# click.echo() cursor.lastrowid
	cursor.close()
	conn.commit()
	conn.close()

	click.echo(buysell+' '+str(amount)+' share of ['+stockid+'] during '+str(start_t)+' to '+str(end_t)+' using '+alg+' algorithm')
	
@click.command()
@click.option('--orderid', help='The ID of the order you want to show')
@click.option('--stockid', help='The ID of the stock you want to show')
@click.option('--sql', help='Costomized SQL query')
def showorder(orderid, stockid, sql):
	"""Show the detail of orders placed"""
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	if sql != None:
		cursor.execute(sql)
	elif orderid != None:
		click.echo('Retrieving order No.'+str(orderid)+'...')
		# get it from DB
		cursor.execute('select * from orders where id=?',(str(orderid),))
	elif stockid != None:
		click.echo('Retrieving orders of Stock '+str(stockid)+'...')
		# get them from DB
		cursor.execute('select * from orders where stockid=?',(str(stockid),))
		# cursor.execute('select * from orders where stockid=100100')
	else:
		click.echo('Retrieving all orders...')
		# click.echo() all
		cursor.execute('select * from orders')
	values = cursor.fetchall()
	click.echo('   B/S   Stock    Amt       Start Time             End Time      Alg.  Staus')
	for row in values:
		click.echo(str(row[0])+'  '+row[1]+'  '+row[2]+'  '+str(row[5])+'  '+row[3]+'  '+row[4]+'  '+row[6]+'    '+str(row[7]))
	cursor.close()
	conn.close()

@click.command()
@click.option('--orderid', prompt=True, help='The ID of the order you want to delete')
@click.confirmation_option(help='Are you sure to DELETE this order?')
def deleteorder(orderid):
	"""Delete order by order ID"""
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	cursor.execute('delete from orders where id=?',(str(orderid),))
	cursor.close()
	conn.commit()
	conn.close()	

@click.command()
def run():	
	"""Execute new placed orders"""
	orderlist = []
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	cursor.execute('select * from orders where status=0')
	values = cursor.fetchall()
	for row in values:
		orderlist.append(clientOrder(row[0],row[2],datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S'),datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S'),row[3],row[6],row[1],1,1))
		#pass to algo trading
	singletrade = algo_trading(orderlist[0])
	singletrade.getQuantAnalysisResult()
	singletrade.tradeRequest()
	cursor.execute('update orders set status=1 where status=0')
	cursor.close()
	conn.commit()
	conn.close()

@click.command()
@click.option('--orderid', help='The ID of the order you want to show')
@click.option('--stockid', help='The ID of the stock you want to show')
def showresult(orderid, stockid):
	"""Show the result of order execution"""
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	if orderid != None:
		click.echo('Retrieving result of order No.'+str(orderid)+'...')
		# get it from DB
		cursor.execute('select id,buysell,stockid,amount,alg,total,ap,wap from orders where id=?',(str(orderid),))
	elif stockid != None:
		click.echo('Retrieving results of Stock '+str(stockid)+'...')
		# get them from DB
		cursor.execute('select id,buysell,stockid,amount,alg,total,ap,wap from orders where stockid=?',(str(stockid),))
		# cursor.execute('select * from orders where stockid=100100')
	else:
		click.echo('Retrieving all results...')
		# click.echo() all
		cursor.execute('select id,buysell,stockid,amount,alg,total,ap,wap from orders')
	values = cursor.fetchall()
	click.echo('   B/S   Stock   Amt  Tuneover AP  Alg  WAP')
	#print values
	for row in values:
		click.echo(str(row[0])+'  '+row[1]+'  '+row[2]+'  '+str(row[3])+'  '+str(row[5])+'  '+str(row[6])+'  '+str(row[4])+'  '+str(row[7]))
	cursor.close()
	conn.close()

cli.add_command(initdb)
cli.add_command(placeorder)
cli.add_command(showorder)
cli.add_command(deleteorder)
cli.add_command(run)
cli.add_command(showresult)

if __name__ == "__main__":
	cli()
