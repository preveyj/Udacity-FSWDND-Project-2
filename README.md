Jesse Prevéy

Udacity Full Stack Web Developer Nanodegree Project 2


INSTRUCTIONS:

To run this file, you'll need Vagrant and VirtualBox installed.

VirtualBox can be downloaded here: https://www.virtualbox.org/wiki/Downloads
Vagrant can be found here: https://www.vagrantup.com/downloads.html

Once you have Vagrant and VirtualBox up and running, open a command prompt and 
navigate to vagrant/ inside this directory, and run the following commands:

vagrant up
vagrant ssh

That will install and configure the Vagrant VM needed for this project, and log 
into an SSH session on the VM.  Once you're logged in, run the following
command:

psql -f /vagrant/tournament/tournament.sql

That will seed the PostgreSQL database for the tournament to use, and is 
required for the tests to work.  To run the tests, run the following command:

python /vagrant/tournament/tournament_test.py



Extra Credit:

Only some of the extra credit features are implemented:

-Support for draws is built into the tournament.sql database, but not used in 
the test.
-Ranking by opponent match wins is implemented in the database.

Multiple tournaments and 'byes' are supported in tournament_extra.sql, but 
tournament.py and tournament_test.py do not implement these features.  The 
tournament_extra.sql database implements multiple tournaments via 
tbl_tournaments and vw_current_tournament, providing a table to record 
tournaments and a view to show what the current tournament is, along with 
foreign key references to Tournament in tbl_players and tbl_matches.

"Byes" are supported via recording a match where the winner_id is the player id
of the player getting the "bye" and the loser_id is 0.  