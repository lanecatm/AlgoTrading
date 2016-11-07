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
from clientOrder import clientOrder
from datetime import datetime
import sqlite3



dbfile = 'test1.db'


@click.group()
def cli():
	pass

@click.command()
def initdb():
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	# Create Table Orders
	cursor.execute('create table orders (id integer primary key autoincrement, buysell text, stockid text, start text, end text, amount int, alg text)')
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
	click.echo('Placing Order...')
	
	# transfer time format
	if starttime is None:
		starttime = '9:00:00'
	if endtime is None:
		endtime = '15:00:00'
	start_t = datetime.strptime(start+' '+starttime, '%Y-%m-%d %H:%M:%S')
	end_t = datetime.strptime(end+' '+endtime, '%Y-%m-%d %H:%M:%S')
	# print start_t 
	# print end_t

	# store as an object
	# order = clientOrder(buysell, stockid, start_t, end_t, amount, alg)

	# store into database
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	
	# Create table, only at 1st time runned. 
	
	cursor.execute(r'insert into orders (buysell, stockid, start, end, amount, alg) values (?,?,?,?,?,?)',(buysell, stockid, str(start_t), str(end_t), str(amount), alg))
	# print cursor.lastrowid
	
	# cursor.execute('select * from orders')
	# values = cursor.fetchall()
	# print values

	cursor.close()
	conn.commit()
	conn.close()

	click.echo(buysell+' '+str(amount)+' share of ['+stockid+'] during '+str(start_t)+' to '+str(end_t)+' using '+alg+' algorithm')
	
@click.command()
@click.option('--orderid', help='The ID of the order you want to show')
@click.option('--stockid', help='The ID of the stock you want to show')
@click.option('--sql', help='Costomized SQL query')
def showorder(orderid, stockid):
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	if sql != None:
		cursor.execute(sql)
	elif orderid != None:
		print 'Retrieving order No.'+str(orderid)+'...'
		# get it from DB
		cursor.execute('select * from orders where id=?',(str(orderid),))
	elif stockid != None:
		print 'Retrieving orders of Stock '+str(stockid)+'...'
		# get them from DB
		cursor.execute('select * from orders where stockid=?',(str(stockid),))
		# cursor.execute('select * from orders where stockid=100100')
	else:
		print 'Retrieving all orders...'
		# print all
		cursor.execute('select * from orders')
	values = cursor.fetchall()
	print '   B/S   Stock  Amt       Start Time             End Time      Alg.'
	for row in values:
		print str(row[0])+'  '+row[1]+'  '+row[2]+'  '+str(row[5])+'  '+row[3]+'  '+row[4]+'  '+row[6]
	cursor.close()
	conn.close()

@click.command()
@click.option('--orderid', prompt=True, help='The ID of the order you want to delete')
@click.confirmation_option(help='Are you sure to DELETE this order?')
def deleteorder(orderid):
	# TBD
	# if : # check id
	# 	# delete from db
	# else:
	# 	print 'Error. No such order named'+str(orderid)
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	cursor.execute('delete from orders where id=?',(str(orderid),))
	cursor.close()
	conn.commit()
	conn.close()	

@click.command()
def run():
	# pass order to AlgoTrading module
	pass

@click.command()
@click.option('--orderid', help='The ID of the order you want to show')
@click.option('--stockid', help='The ID of the stock you want to show')
def showresult(orderid, stockid):
	if orderid != None:
		print 'Retrieving result of order No.'+str(orderid)+'...'
		# get it from DB
	else: 
		if stockid != None:
			print 'Retrieving results of of Stock '+str(stockid)+'...'
			# get them from DB
		else:
			print 'Retrieving all results...'
			# print all


cli.add_command(placeorder)
cli.add_command(showorder)
cli.add_command(deleteorder)
cli.add_command(run)
cli.add_command(showresult)

if __name__ == "__main__":
	cli()
