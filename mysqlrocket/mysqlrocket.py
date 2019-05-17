#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from builtins import input
from mysqlrocket import ressources
import sys
import configparser
import string
import random
import datetime
import subprocess
from appdirs import *
from argparse import ArgumentParser
import MySQLdb as mysql


def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
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
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


class MySQLRocketDB(object):
    def __init__(self):
        self.name = ""
        self.size = ""
        self.tables_number = ""
        self.rows_number = ""


class MySQLRocket(object):
    appname = "mysqlrocket"
    appauthor = ressources.__author__

    def __init__(self):
        self.name = "default"
        self.host = "localhost"
        self.user = "root"
        self.port = "3306"
        self.password = ""
        self.mysql = "/usr/bin/mysql"
        self.mysqldump = "/usr/bin/mysqldump"
        self.excluded = "information_schema performance_schema"
        self.config = configparser.ConfigParser()
        self.config_file = os.path.join(
            user_data_dir(self.appname, self.appauthor), "mysqlrocket.cfg"
        )
        self.config.read(self.config_file)

    def config_remove(self, config_id):
        remove_config = query_yes_no("Are you sure you want to remove config?")
        if remove_config:
            self.config.remove_section(config_id)
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)
                print(
                    "\nConfiguration file has been update: "
                    + os.path.abspath(self.config_file)
                )

    def db_exist(self, db_name):
        db_list = self.showdb("%")
        for database in db_list:
            if database == db_name:
                return True
        return False

    def load(self, config_id):
        if self.config.has_section(config_id):
            try:
                self.host = self.config.get(config_id, "host")
                self.port = int(self.config.get(config_id, "port"))
                self.user = self.config.get(config_id, "user")
                self.password = self.config.get(config_id, "password")
                self.mysql = self.config.get(config_id, "mysql")
                self.mysqldump = self.config.get(config_id, "mysqldump")
                self.excluded = self.config.get(config_id, "excluded")
            except configparser.NoOptionError:
                print("Invalid or outdated config")
                remove_config = query_yes_no("Do you want to remove invalid config")
                if remove_config:
                    self.config_remove(config_id)
                sys.exit(1)
        else:
            print(
                "Please provide MySQL connection informations: host, port, user, pass. ".center(
                    50, "+"
                )
            )
            input_host = input("host (" + self.host + ")> ")
            input_port = input("port (" + str(self.port) + ")> ")
            input_user = input("user (" + self.user + ")> ")
            input_password = input("pass > ")
            input_mysql = input("mysql absolute path (" + self.mysql + ")> ")
            input_mysqldump = input(
                "mysqldump absolute path (" + self.mysqldump + ")> "
            )
            save_config = query_yes_no("Do you want to save configuration?")
            if save_config:
                self.config.add_section(config_id)
                self.config.set(config_id, "name", self.name)
                if input_host:
                    self.config.set(config_id, "host", input_host)
                    self.host = input_host
                else:
                    self.config.set(config_id, "host", self.host)
                if input_port:
                    self.config.set(config_id, "port", input_port)
                    self.port = input_port
                else:
                    self.config.set(config_id, "port", self.port)
                if input_user:
                    self.config.set(config_id, "user", input_user)
                    self.user = input_user
                else:
                    self.config.set(config_id, "user", self.user)
                if input_password:
                    self.config.set(config_id, "password", input_password)
                    self.password = input_password
                else:
                    self.config.set(config_id, "password", self.password)
                if input_mysql:
                    self.config.set(config_id, "mysql", input_mysql)
                    self.mysql = input_mysql
                else:
                    self.config.set(config_id, "mysql", self.mysql)
                if input_mysqldump:
                    self.config.set(config_id, "mysqldump", input_mysqldump)
                    self.mysqldump = input_mysqldump
                else:
                    self.config.set(config_id, "mysqldump", self.mysqldump)
                self.config.set(config_id, "excluded", self.excluded)
                if not os.path.exists(os.path.dirname(self.config_file)):
                    os.makedirs(os.path.dirname(self.config_file))
                with open(self.config_file, "w") as configfile:
                    self.config.write(configfile)
                    print(
                        "\nConfiguration file has been saved to: "
                        + os.path.abspath(self.config_file)
                    )
                    print("WARNING: password has been stored in plain text \n")
                os.chmod(self.config_file, 0o640)

    def mk(self, db_name, db_password):
        if self.db_exist(db_name):
            print("(Error database already exist!")
            sys.exit(1)
        db_user = db_name
        if len(db_user) > 16:
            print(
                "ERROR user name (same as datatabase name) cannot exceed 16 characters (MySQL restriction)"
            )
            sys.exit(1)
        dictionnary = (
            string.ascii_letters + string.digits
        )  # alphanumeric, upper and lowercase
        if db_password == "":
            db_password = "".join([random.choice(dictionnary) for i in range(8)])
        try:
            conn = mysql.connect(
                host=self.host,
                port=int(self.port),
                user=self.user,
                passwd=self.password,
            )
            cursor = conn.cursor()
            cursor.execute(
                "CREATE DATABASE {database_name};".format(database_name=db_name)
            )
            cursor.execute(
                "GRANT ALL ON {database_name}.* TO {username}@{host} IDENTIFIED BY '{password}'".format(
                    database_name=db_name,
                    username=db_user,
                    host=self.host,
                    password=db_password,
                )
            )
            cursor.execute("FLUSH PRIVILEGES;")
            cursor.close()
            conn.close()
        except mysql.Error as e:
            print("Database creation fail")
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        print("-" * 80)
        print("| {0:76} |".format("Database was successfully created!"))
        print("-" * 80)
        print("* {0}".format("Host: " + self.host))
        print("* {0}".format("Database: " + db_name))
        print("* {0}".format("User: " + db_user))
        print("* {0}".format("Password: " + db_password))
        print(
            "* {0}".format(
                "DSN: mysql://"
                + db_user
                + ":"
                + db_password
                + "@"
                + self.host
                + "/"
                + db_name
            )
        )
        print("-" * 80)

    def ls(self, db_pattern="%", db_extend=False):
        db_list = self.showdb(db_pattern)
        db_list.sort()
        if db_extend:
            print("-" * 80)
            print(
                "| {0:28}| {1:16}| {2:15}| {3:12}|".format(
                    "Database", "Tables number", "Rows number", "Size (MB)"
                )
            )
            print("-" * 80)
        else:
            print("-" * 31)
            print("| {0:28}|".format("Database"))
            print("-" * 31)
        for database in db_list:
            if db_extend:
                db = self.get_db_properties(database)
                print(
                    "| {0:28}| {1:16}| {2:15}| {3:12}|".format(
                        db.name[:20],
                        db.tables_number[:20],
                        db.rows_number[:8],
                        db.size[:30],
                    )
                )
            else:
                print("| {0:28}|".format(database[:20]))
        if db_extend:
            print("-" * 80)
        else:
            print("-" * 31)

    def showdb(self, db_pattern="%"):
        db_list = []
        try:
            conn = mysql.connect(
                host=self.host,
                port=int(self.port),
                user=self.user,
                passwd=self.password,
            )
            cursor = conn.cursor()
            cursor.execute(
                "SHOW DATABASES LIKE '{pattern}';".format(pattern=db_pattern)
            )
            for database in cursor.fetchall():
                db_list.append(database[0])
            cursor.close()
            conn.close()
        except mysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        return db_list

    def rm(self, db_name):
        if not self.db_exist(db_name):
            print(
                'Database "{database_name}" do not exist, operation aborted!'.format(
                    database_name=db_name
                )
            )
            exit()
        print(
            'Database "{database_name}" will be deleted'.format(database_name=db_name)
        )
        areyousure = query_yes_no("Are you sure?", "no")
        if areyousure is False:
            print("Operation aborted")
            exit()
        protected_db = ["information_schema", "mysql", "information_schema"]
        if any(db_name == db for db in protected_db):
            print('"' + db_name + '" is a protected database, you should not delete it')
            exit()
        try:
            conn = mysql.connect(
                host=self.host,
                port=int(self.port),
                user=self.user,
                passwd=self.password,
            )
            cursor = conn.cursor()
            cursor.execute(
                "DROP DATABASE {database_name};".format(database_name=db_name)
            )
            cursor.execute(
                "DROP USER {username}@{host};".format(username=db_name, host=self.host)
            )
            cursor.close()
            conn.close()
        except mysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        print("-" * 50)
        print("| {0:46} |".format("Database was successfully deleted!"))
        print("-" * 50)

    def dp(self, db_name, dp_dest):
        datenow = datetime.datetime.now()
        filename = (
            dp_dest
            + db_name
            + "-"
            + datenow.strftime("%Y_%m_%d-%H_%M_%S")
            + ".sql"
            + ".gz"
        )
        try:
            if self.password == "":
                p1 = subprocess.Popen(
                    self.mysqldump
                    + " -u %s -h %s -e --opt --single-transaction --max_allowed_packet=512M -c %s"
                    % (self.user, self.host, db_name),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                )
            else:
                p1 = subprocess.Popen(
                    self.mysqldump
                    + " -u %s -p%s -h %s -e --opt --single-transaction --max_allowed_packet=512M -c %s"
                    % (self.user, self.password, self.host, db_name),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                )
            p2 = subprocess.Popen(
                "gzip -c > %s" % (filename), stdin=p1.stdout, shell=True
            )
            p1.stdout.close()
            output = p1.stderr.read()
            if output == "":
                print("The database has been dump to: " + filename)
            else:
                print(output)
                exit(1)
        except subprocess.CalledProcessError as e:
            print("Error: process exited with status %s" % e.returncode)

    def fs(self, db_name):
        print(
            'Database "{database_name}" will be flushed, and all its content deleted'.format(
                database_name=db_name
            )
        )
        areyousure = query_yes_no("Are you sure?", "no")
        if areyousure is False:
            print("Operation aborted")
            exit()
        protected_db = ["information_schema", "mysql", "information_schema"]
        if any(db_name == db for db in protected_db):
            print('"' + db_name + " is a protected database, you should not delete it")
            exit()
        try:
            conn = mysql.connect(
                host=self.host,
                port=int(self.port),
                user=self.user,
                passwd=self.password,
            )
            cursor = conn.cursor()
            cursor.execute(
                "DROP DATABASE {database_name};".format(database_name=db_name)
            )
            cursor.execute(
                "CREATE DATABASE {database_name};".format(database_name=db_name)
            )
            cursor.close()
            conn.close()
        except mysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        print("-" * 50)
        print("| {0:46} |".format("Database was successfully flushed!"))
        print("-" * 50)

    def cp(self, db_src, db_dest):
        if not self.db_exist(db_dest):
            print(
                'Database "{database_name}" do not exist, do you want to create it?'.format(
                    database_name=db_dest
                )
            )
            areyousure = query_yes_no("Are you sure?", "no")
            if areyousure is False:
                print("Operation aborted")
                exit()
            self.mk(db_dest, "")
        else:
            self.fs(db_dest)
        try:
            if self.password == "":
                p1 = subprocess.Popen(
                    self.mysqldump
                    + " -u %s -h %s -e --opt --single-transaction --max_allowed_packet=512M -c %s"
                    % (self.user, self.host, db_src),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                )
                p2 = subprocess.Popen(
                    self.mysql + " -u %s -h %s %s" % (self.user, self.host, db_dest),
                    stdin=p1.stdout,
                    shell=True,
                )
            else:
                p1 = subprocess.Popen(
                    self.mysqldump
                    + " -u %s -p%s -h %s -e --opt --single-transaction --max_allowed_packet=512M -c %s"
                    % (self.user, self.password, self.host, db_src),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                )
                p2 = subprocess.Popen(
                    self.mysql
                    + " -u %s -p%s -h %s %s"
                    % (self.user, self.password, self.host, db_dest),
                    stdin=p1.stdout,
                    shell=True,
                )
            p1.stdout.close()
            output = p1.stderr.read()
            if output == "":
                print("The database " + db_src + " has been duplicate to: " + db_dest)
            else:
                print(output)
                exit(1)
        except subprocess.CalledProcessError as e:
            print("Error: process exited with status %s" % e.returncode)

    def ld(self, db_name, fl_name):
        if not os.path.exists(fl_name):
            print(
                'File "{file_name}" do not exist, operation aborted!'.format(
                    file_name=fl_name
                )
            )
            exit()
        if not self.db_exist(db_name):
            print(
                'Database "{database_name}" do not exist, do you want to create it?'.format(
                    database_name=db_name
                )
            )
            areyousure = query_yes_no("Are you sure?", "no")
            if areyousure is False:
                print("Operation aborted")
                exit()
            self.mk(db_name, "")
        else:
            self.fs(db_name)
        try:
            if self.password == "":
                p1 = subprocess.Popen(
                    self.mysql + " -u %s -h %s %s" % (self.user, self.host, db_name),
                    stdin=open(fl_name, "r"),
                    shell=True,
                )
            else:
                p1 = subprocess.Popen(
                    self.mysql
                    + " -u %s -p%s -h %s %s"
                    % (self.user, self.password, self.host, db_name),
                    stdin=open(fl_name, "r"),
                    shell=True,
                )
            print(fl_name + " has been imported to: " + db_name)
        except subprocess.CalledProcessError as e:
            print("Error: process exited with status %s" % e.returncode)

    def st(self, st_extended=False):
        try:
            conn = mysql.connect(
                host=self.host,
                port=int(self.port),
                user=self.user,
                passwd=self.password,
            )
            cursor = conn.cursor()
            print("MySQL connection was successful!")
            if st_extended:
                cursor.execute("SHOW STATUS;")
                print("-" * 50)
                print("| {0:46} |".format("MySQL Server Status"))
                print("-" * 50)
                for status in cursor.fetchall():
                    print(" " + status[0] + " = " + status[1])
                print("-" * 50)
            cursor.close()
            conn.close()
        except mysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)

    def get_db_properties(self, db_name):
        db = MySQLRocketDB()
        db.name = db_name
        try:
            conn = mysql.connect(
                host=self.host,
                port=int(self.port),
                user=self.user,
                passwd=self.password,
            )
            cursor = conn.cursor()
            cursor.execute(
                'SELECT count(*) FROM information_schema.tables WHERE TABLE_SCHEMA="{database_name}";'.format(
                    database_name=db.name
                )
            )
            result = cursor.fetchone()
            db.tables_number = str(result[0])
            cursor.execute(
                'SELECT SUM(TABLE_ROWS) FROM information_schema.tables WHERE TABLE_SCHEMA="{database_name}";'.format(
                    database_name=db.name
                )
            )
            result = cursor.fetchone()
            db.rows_number = str(result[0])
            cursor.execute(
                'SELECT ROUND(SUM( data_length + index_length ) / 1024 / 1024, 3) FROM information_schema.tables WHERE TABLE_SCHEMA="{database_name}";'.format(
                    database_name=db.name
                )
            )
            result = cursor.fetchone()
            db.size = str(result[0])
            cursor.close()
            conn.close()
        except mysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        return db


def launcher():
    parser = ArgumentParser(
        description=ressources.__description__, prog=ressources.__app_name__
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s : " + ressources.__version__,
        help="Show program version.",
    )
    parser.add_argument(
        "-u", dest="mysql_user", metavar="<mysql_user>", type=str, help="mysql user"
    )
    parser.add_argument(
        "-H", dest="mysql_host", metavar="<mysql_host>", type=str, help="mysql host"
    )
    parser.add_argument(
        "-p",
        dest="mysql_password",
        metavar="<mysql_password>",
        type=str,
        help="mysql password",
    )
    parser.add_argument(
        "-P", dest="mysql_port", metavar="<mysql_user>", type=int, help="mysql port"
    )

    subparsers = parser.add_subparsers(help="Avalaible commands")

    session = MySQLRocket()
    session.load("Server1")

    parser_mk = subparsers.add_parser(
        "mk", description="Create a MySQL database", help="Create a MySQL database"
    )
    parser_mk.add_argument(
        "mk_db_name", metavar="<db_name>", type=str, help="Name of the created database"
    )
    parser_mk.add_argument(
        "-f",
        "--force-password",
        dest="mk_db_pass",
        metavar="<new_user_password>",
        type=str,
        default="",
        help="Override random password generation",
    )

    parser_ls = subparsers.add_parser(
        "ls",
        description="Show databases on MySQL server",
        help="Show databases on MySQL server",
    )
    parser_ls.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="ls_db_extend",
        help="Show detailed information for each database",
    )
    parser_ls.add_argument(
        "ls_db_pattern",
        metavar="<search_pattern>",
        type=str,
        nargs="?",
        default="%",
        help="Show only databases name matching pattern",
    )

    parser_rm = subparsers.add_parser(
        "rm", description="Delete a MySQL database", help="Delete a MySQL database"
    )
    parser_rm.add_argument(
        "rm_db_name", metavar="<db_name>", type=str, help="Name of the deleted database"
    )

    parser_dp = subparsers.add_parser(
        "dp", description="Dump a MySQL database", help="Dump a MySQL database"
    )
    parser_dp.add_argument(
        "dp_db_name", metavar="<db_name>", type=str, help="Name of the dumped database"
    )
    parser_dp.add_argument(
        "-d",
        "--force-destination",
        dest="dp_dest",
        metavar="<dump_destination>",
        type=str,
        default="",
        help="Dump to a specific destination",
    )

    parser_bk = subparsers.add_parser(
        "bk",
        description="Backup all databases on MySQL server",
        help="Backup all databases on MySQL server",
    )
    parser_bk.add_argument(
        "bk_db_pattern",
        metavar="<backup_pattern>",
        type=str,
        nargs="?",
        default="%",
        help="Dump only databases name matching pattern",
    )
    parser_bk.add_argument(
        "-d",
        "--force-destination",
        dest="bk_dest",
        metavar="<backup_destination>",
        type=str,
        default="",
        help="Backup to a specific destination",
    )

    parser_fs = subparsers.add_parser(
        "fs", description="Flush a MySQL database", help="Flush a MySQL database"
    )
    parser_fs.add_argument(
        "fs_db_name", metavar="<db_name>", type=str, help="Name of the flushed database"
    )

    parser_cp = subparsers.add_parser(
        "cp",
        description="Duplicate a MySQL database",
        help="Duplicate a MySQL database",
    )
    parser_cp.add_argument(
        "cp_db_src", metavar="<db_src>", type=str, help="Source database"
    )
    parser_cp.add_argument(
        "cp_db_dest", metavar="<db_dest>", type=str, help="Destination database"
    )

    parser_ld = subparsers.add_parser(
        "ld",
        description="Load a MySQL database from a file",
        help="Load a MySQL database from a file",
    )
    parser_ld.add_argument(
        "ld_db_name", metavar="<db_name>", type=str, help="Name of the database"
    )
    parser_ld.add_argument(
        "ld_fl_name", metavar="<fl_name>", type=str, help="File to import"
    )

    parser_st = subparsers.add_parser(
        "st",
        description="Check your mysqlrocket config file and MySQL server status",
        help="Check your mysqlrocket config file and MySQL server status",
    )
    parser_st.add_argument(
        "st_extended",
        metavar="<status>",
        type=str,
        nargs="?",
        default="basic",
        help='Choose between "basic" or "full" status',
    )

    args = parser.parse_args()

    if args.mysql_user is not None:
        session.user = args.mysql_user

    if args.mysql_host is not None:
        session.host = args.mysql_host

    if args.mysql_password is not None:
        session.password = args.mysql_password

    if args.mysql_port is not None:
        session.port = args.mysql_port

    if hasattr(args, "mk_db_name"):
        session.mk(args.mk_db_name, args.mk_db_pass)

    if hasattr(args, "ls_db_pattern"):
        session.ls("%" + args.ls_db_pattern + "%", args.ls_db_extend)

    if hasattr(args, "rm_db_name"):
        session.rm(args.rm_db_name)

    if hasattr(args, "dp_db_name"):
        session.dp(args.dp_db_name, args.dp_dest)

    if hasattr(args, "bk_db_pattern"):
        db_list = session.showdb(args.bk_db_pattern)
        db_excluded = session.excluded.split()
        for database in db_list:
            if database not in db_excluded:
                session.dp(database, args.bk_dest)

    if hasattr(args, "fs_db_name"):
        session.fs(args.fs_db_name)

    if hasattr(args, "cp_db_src"):
        session.cp(args.cp_db_src, args.cp_db_dest)

    if hasattr(args, "ld_db_name"):
        session.ld(args.ld_db_name, args.ld_fl_name)

    if hasattr(args, "st_extended"):
        if args.st_extended == "full":
            session.st(True)
        else:
            session.st(False)


if __name__ == "__main__":
    launcher()
