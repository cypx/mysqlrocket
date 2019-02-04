***********************************************
MYSQLROCKET  - Simple & fast MySQL manage tool
***********************************************

**MysqlRocket** is a Simple CLI tool to create and delete easily MySQL databases.

usage: mysqlrocket [-h] [-v] [-u U] [-H H] [-p P] {bk,dp,mk,ls,rm,st} ...

mysqlrocket commands are:

* **bk**        Backup all databases on MySQL server
* **dp**        Dump and gzip a MySQL database
* **mk**        Create a MySQL database with an dedicated user and a random password
* **ls**        Show databases on MySQL server
* **rm**        Delete a MySQL database
* **fs**        Flush a MySQL database
* **cp**        Copy a MySQL database to another
* **ld**        Import a dump into a database
* **st**        Check your mysqlrocket config and MySQL server connectivity

Optional arguments:

* **-h, --help**     show this help message and exit
* **-v, --version**  Show program version.
* **-u U**           mysql user
* **-H H**           mysql host
* **-p P**           mysql password

See 'mysqlrocket <command> -h' for more information on a specific command.

PyPI package `<https://pypi.org/project/mysqlrocket/>`__

Sources `<https://github.com/cypx/mysqlrocket>`__

Installation
##############

Install it easily:

Using pip
**************

.. code-block:: bash

	$ pip install mysqlrocket

Using easy_install
*********************

On most Linux distribution

.. code-block:: bash

	$ easy_install mysqlrocket

But on some, prerequisites are required, for example, on Debian (6 to 8)

.. code-block:: bash

	$ apt-get install python-pip python-mysqldb libmysqlclient-dev

(mysqldb could not be installed by easy_install cause of some system dependencies)

Manual install
*********************

.. code-block:: bash

	$ git clone https://github.com/cypx/mysqlrocket
	$ cd mysqlrocket
	$ python setup.py install

Upgrade
##########

Using pip
**************

.. code-block:: bash

	$ pip install mysqlrocket --upgrade

Using easy_install
*********************

.. code-block:: bash

	$ easy_install --upgrade mysqlrocket

Uninstall
##########

Using pip
**************

.. code-block:: bash

	$ pip uninstall mysqlrocket

Examples
##########

Create a new database
*************************

Create a new database with an associated user account using the same name and a random password

.. code-block:: bash

	$ mysqlrocket mk DATABASE_NAME

Create a new database with an associated user account using the same name and force password

.. code-block:: bash

	$ mysqlrocket mk DATABASE_NAME -f DATABASE_PASSWORD

Backup databases
*************************

Dump all databases available on your server to the current directory

.. code-block:: bash

	$ mysqlrocket bk

Dump database
*************************

Dump a databases to the current directory

.. code-block:: bash

	$ mysqlrocket dp DATABASE_NAME


Show all databases
*************************

Show all databases available on your server

.. code-block:: bash

	$ mysqlrocket ls

Show all databases available on your server and some information (tables number, size...)

.. code-block:: bash

	$ mysqlrocket ls -a

Remove a database
*************************

Remove a database and all user account with the same name if they exist

.. code-block:: bash

	$ mysqlrocket rm DATABASE_NAME

Copy a database
*************************

Copy a database to another (flush destination database if its exist, create if not)

.. code-block:: bash

	$ mysqlrocket cp SOURCE_DATABASE_NAME DESTINATION_DATABASE_NAME

Load dump file to database
*******************************

Load dump file to database (flush destination database if its exist, create if not)

.. code-block:: bash

	$ mysqlrocket ld SOURCE_DATABASE_NAME FILE_PATH


Flush a database
*************************

Flush a database (all content will be deleted)

.. code-block:: bash

	$ mysqlrocket fs DATABASE_NAME

Check mysqlrocket configuration
************************************

Check your mysqlrocket config file and MySQL server connectivity

.. code-block:: bash

	$ mysqlrocket st
