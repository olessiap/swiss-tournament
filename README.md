# swiss-tournament
A database schema that stores game matches between players using the Swiss System for player pairing. 

### Instructions 

download [Vagrant](https://www.vagrantup.com/docs/installation/)

download [Virtual Box](https://www.virtualbox.org/)

`cd` into the `swiss-tournament` directory

run `vagrant up` to start running the virtual machine 

`vagrant ssh` to log into the vm 

`cd /vagrant/tournament/` to access the necessary files

`psql -f tournament.sql` to create the database and tables

`python tournament_test.py` to see the program pass all the tests with flying colors. 



