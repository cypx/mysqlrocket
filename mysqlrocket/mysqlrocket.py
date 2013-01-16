#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ressources

import sys
import ConfigParser
import string
import random
import datetime
from appdirs import *
from argparse import ArgumentParser
import MySQLdb as mysql


def query_yes_no(question, default="yes"):
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")


class mysqlrocket:
	name = "default"
	host = "localhost"
	user = "root"
	port = 3306
	password = ""
	config = ConfigParser.ConfigParser()
	configfile = ""

	def __init__(self):
		appname = "mysqlrocket"
		appauthor = ressources.__author__
		self.config_file= os.path.join(user_data_dir(appname, appauthor), 'mysqlrocket.cfg')
		self.config.read(self.config_file)

	def config_remove(self, config_id):
			remove_config=query_yes_no("Are you sure you want to remove config?")
			if (remove_config):
				self.config.remove_section(config_id)
				with open(self.config_file, 'wb') as configfile:
					self.config.write(configfile)
					print '\nConfiguration file has been update: '+os.path.abspath(self.config_file)


	def load(self, config_id):
		if (self.config.has_section(config_id)):
			try:
				self.host=self.config.get(config_id, 'host', 0)
				self.port=int(self.config.get(config_id, 'port', 0))
				self.user=self.config.get(config_id, 'user', 0)
				self.password=self.config.get(config_id, 'password', 0)
			except ConfigParser.NoOptionError:
				print 'Invalid or outdated config'
				remove_config=query_yes_no("Do you want to remove invalid config")
				if (remove_config):
					self.config_remove(config_id)
				sys.exit(1)
		else:
			print "Please provide MySQL connection informations: host, port, user, pass. ".center(50, "+")
			input_host = raw_input("host ("+self.host+")> ")
			input_port = raw_input("port ("+str(self.port)+")> ")
			input_user = raw_input("user ("+self.user+")> ")
			input_password = raw_input("pass > ")
			save_config=query_yes_no("Do you want to save configuration?")
			if (save_config):
				self.config.add_section(config_id)
				self.config.set(config_id, 'name', self.name)
				if input_host:
					self.config.set(config_id, 'host', input_host) 
				else:
					self.config.set(config_id, 'host', self.host)
				if input_port:
					self.config.set(config_id, 'port', int(input_port))
				else:
					self.config.set(config_id, 'port', self.port)
				if input_user:
					self.config.set(config_id, 'user', input_user)
				else:
					self.config.set(config_id, 'user', self.user)
				self.config.set(config_id, 'password', input_password)
				if not os.path.exists(os.path.dirname(self.config_file)):
					os.makedirs(os.path.dirname(self.config_file))
				with open(self.config_file, 'wb') as configfile:
					self.config.write(configfile)
					print '\nConfiguration file has been saved to: '+os.path.abspath(self.config_file)
					print 'WARNING: password has been stored in plain text \n'

	def mk(self, db_name, db_password):
		db_user=db_name
		dictionnary=string.ascii_letters+string.digits # alphanumeric, upper and lowercase
		if db_password=='':
			db_password="".join([random.choice(dictionnary) for i in range(8)])
		try:
			# Establish MySQL connection
			conn = mysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password)
			cursor = conn.cursor()

			# Execute database and user creation queries
			cursor.execute('CREATE DATABASE {database_name};'.format(database_name=db_name))
			cursor.execute("GRANT ALL ON {database_name}.* TO {username}@{host} IDENTIFIED BY '{password}'".format(database_name=db_name, username=db_user, host=self.host, password=db_password))
			cursor.execute('FLUSH PRIVILEGES;')

			# Clean up the connections
			cursor.close()
			conn.close()

		except mysql.Error, e:	
			print "Database creation fail"
			print('Error %d: %s' % (e.args[0], e.args[1]))
			sys.exit(1)
		print '##################################'			
		print "Database was successfully created!"
		print '##################################'
		print "Host: "+self.host
		print "Database name: "+db_name
		print "User name: "+db_user
		print "User password: "+db_password
		print "DSN: mysql://"+db_user+":"+db_password+"@"+self.host+"/"+db_name
		print '##################################'

	def ls(self, db_pattern='%'):
		try:
			# Establish MySQL connection
			conn = mysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password)
			cursor = conn.cursor()

			# Show databases
			cursor.execute("SHOW DATABASES LIKE '{pattern}';".format(pattern=db_pattern))

			print '##################################'
			print '#        Database list           #'
			print '##################################'
			for database in cursor.fetchall():
				print '  '+database[0]
			print '##################################'

			# Clean up the connections
			cursor.close()
			conn.close()

		except mysql.Error, e:
			print('Error %d: %s' % (e.args[0], e.args[1]))
			sys.exit(1)


	def rm(self, db_name):
		print db_name
		print 'Database "{database_name}" will be deleted'.format(database_name=db_name)
		areyousure=query_yes_no('Are you sure?','no')
		if areyousure is False:
			print 'Operation aborted'
			exit()
		protected_db=['information_schema', 'mysql', 'information_schema']
		if any(db_name == db for db in protected_db):
			print '"'+db_name+'" is a protected database, you should not delete it'
			exit()
		try:
			# Establish MySQL connection
			conn = mysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password)
			cursor = conn.cursor()

			# Show databases
			cursor.execute('DROP DATABASE {database_name};'.format(database_name=db_name))
			cursor.execute('DROP USER {username}@{host};'.format(username=db_name, host=self.host))

			# Clean up the connections
			cursor.close()
			conn.close()

		except mysql.Error, e:
			print('Error %d: %s' % (e.args[0], e.args[1]))
			sys.exit(1)
		print '##################################'			
		print "Database was successfully deleted!"
		print '##################################'

	def st(self, st_extended=False):
		try:
			# Establish MySQL connection
			conn = mysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password)
			cursor = conn.cursor()

			print 'MySQL connection was successful!'

			if st_extended:
				# Show databases
				cursor.execute('SHOW STATUS;')

				print '##################################'
				print '#       MySQL Server Status      #'
				print '##################################'
				for status in cursor.fetchall():
					print '  '+status[0]+' = '+status[1]
				print '##################################'

			# Clean up the connections
			cursor.close()
			conn.close()

		except mysql.Error, e:
			print('Error %d: %s' % (e.args[0], e.args[1]))
			sys.exit(1)
		#your code goes here



def launcher():
	parser = ArgumentParser(description=ressources.__description__,prog="mysqlrocket")

	parser.add_argument("-v", "--version",  action="version",   version="%(prog)s : "+ressources.__version__ ,help="Show program version.")
	parser.add_argument('-u', type=str, default='root', help='mysql user')
	parser.add_argument('-H', type=str, default='localhost', help='mysql host')
	parser.add_argument('-p', type=str, default='', help='mysql password')


	subparsers = parser.add_subparsers(help='Avalaible commands')

	session=mysqlrocket()
	session.load('Server1')

	parser_mk = subparsers.add_parser('mk',description='Create a MySQL database', help='Create a MySQL database')
	parser_mk.add_argument('mk_db_name', metavar='<db_name>', type=str, help='Name of the created database')
	parser_mk.add_argument('-f', '--force-password',dest='mk_db_pass', type=str, default='', help='Override random password generation')

	parser_ls = subparsers.add_parser('ls', description='Show databases on MySQL server', help='Show databases on MySQL server')
	parser_ls.add_argument('ls_db_pattern', metavar='<search_pattern>', type=str, nargs='?', default='%', help='Show only databases name matching pattern')

	parser_rm = subparsers.add_parser('rm',description='Delete a MySQL database', help='Delete a MySQL database')
	parser_rm.add_argument('rm_db_name', type=str, help='Name of the deleted database')

	parser_st = subparsers.add_parser('st',description='Check your mysqlrocket config file and MySQL server status', help='Check your mysqlrocket config file and MySQL server status')
	parser_st.add_argument('st_extended', metavar='<status>', type=str, nargs='?', default='basic', help='Choose between "basic" or "full" status')

	args = parser.parse_args() 

	if hasattr(args,'mk_db_name'): 
	    session.mk(args.mk_db_name,args.mk_db_pass)

	if hasattr(args,'ls_db_pattern'):
	    session.ls(args.ls_db_pattern)

	if hasattr(args,'rm_db_name'): 
	    session.rm(args.rm_db_name)

	if hasattr(args,'st_extended'):
		if args.st_extended=="full":
			session.st(True)
		else:
			session.st(False)

if __name__ == "__main__":
    launcher()