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

@click.group()
def cli():
	pass

@click.command()
@click.option('--username', prompt=True, default=lambda: os.environ.get('USER', ''))
def hello():
	click.echo('Hello world.')

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
	conn = sqlite3.connect(test.db)
	cursor = conn.cursor()
	cursor.execute('create table orders (id text primary key, buysell text, stockid text, start text, end text, amount int, alg text)')
	orderid = cursor.rowcount + 1
	cursor.execute('insert into orders (id, buysell, stockid, start, end, amount, alg) values (?,?,?,?,?,?,?)',(str(orderid), buysell, stockid, str(start_t), str(end_t), str(amount), alg))
	print cursor.rowcount
	



	# click.echo(order.action+' '+order.stockAmount+' share of ['+order.stockId+'] during '+str(order.startTime)+' to '+str(order.endTime)+' using '+order.algChoice+' algorithm')
	
@click.command()
@click.option('--orderid', help='The ID of the order you want to show')
@click.option('--stockid', help='The ID of the stock you want to show')
def showorder(orderid, stockid):
	if orderid != None:
		print 'Retrieving order No.'+str(orderid)+'...'
		# get it from DB
	else: 
		if stockid != None:
			print 'Retrieving orders of Stock '+str(stockid)+'...'
			# get them from DB
		else:
			print 'Retrieving all orders...'
			# print all
	pass

@click.command()
@click.option('--orderid', prompt=True, help='The ID of the order you want to show')
@click.confirmation_option(help='Are you sure to place this order?')
def deleteorder(orderid):
	# TBD
	# if : # check id
	# 	# delete from db
	# else:
	# 	print 'Error. No such order named'+str(orderid)

	pass

@click.command()
def execorder():
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


cli.add_command(hello)
cli.add_command(placeorder)
cli.add_command(showorder)
cli.add_command(deleteorder)
cli.add_command(execorder)
cli.add_command(showresult)

if __name__ == "__main__":
	cli()
