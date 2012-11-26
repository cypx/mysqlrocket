***********************************************
MYSQLROCKET  - Simple & fast MySQL manage tool 
***********************************************

**MysqlRocket** is a Simple CLI tool to create and delete easily MySQL databases.

usage: mysqlrocket [-h] [-v] [-u U] [-H H] [-p P] {mk,ls,rm,st} ...

mysqlrocket commands are:

* **mk**         Create a MySQL database
* **ls**         Show databases on MySQL server
* **rm**         Delete a MySQL database
* **status**     Check your mysqlrocket config and MySQL server connectivity

Optional arguments:

* **-h, --help**     show this help message and exit
* **-v, --version**  Show program version.
* **-u U**           mysql user
* **-H H**           mysql host
* **-p P**           mysql password

See 'mysqlrocket <command> -h' for more information on a specific command.

Sources `<https://github.com/cypx/mysqlrocket>`__ 

Examples
##########

Create a new database
*************************

Create a new database and an user account with the same name and a random password

.. code-block:: bash

	mysqlrocket mk test_database


Show all databases
*************************

Show all databases avalaible on your server

.. code-block:: bash

	mysqlrocket ls


Remove a database
*************************

Remove a database and all user account with the same name if they exist

.. code-block:: bash

	mysqlrocket rm test_database


Check mysqlrocket configuration
************************************

Check your mysqlrocket config file and MySQL server connectivity

.. code-block:: bash

	mysqlrocket st



