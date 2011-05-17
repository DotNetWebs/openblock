=========================================
Installing and Setting Up the Demo Site
=========================================

These instructions will install the software in a similar configuration to 
`the OpenBlock demo site <http://demo.openblockproject.org>`_ in an isolated 
python environment using `virtualenv <http://pypi.python.org/pypi/virtualenv>`_.


.. _demo_quickstart:

Demo Quickstart
===================

This section will show you how to use our bootstrap scripts to
automatically set up the OpenBlock Boston demo with minimal manual
effort.

Warning
-------

In this quickstart, we use several scripts (python and bash) to
automate a lot of the
installation, configuration, and data bootstrapping. *If it works for
you* this can be the quickest way to try out OpenBlock on your system,
but we are not trying to make it work on all possible variations of linux,
OSX, etc. - so, *caveat emptor*.

Or, if you prefer to have control of how everything's done, follow the
:ref:`detailed_demo_instructions` below.


Installation
------------

First make sure you have the :ref:`requirements` installed.

Next make sure you have :ref:`installed and configured PostGIS <postgis_localhost>`
on the same system (our installer script doesn't support putting
postgis on a remote host, nor can it modify the postgres config file
for you.)

(You can skip the rest of the :doc:`setup` document; everything else
you need will be done automatically by the install scripts.)

Now get the OpenBlock code::

 $ mkdir openblock
 $ cd openblock
 $ mkdir src
 $ git clone git://github.com/openplans/openblock.git src/openblock

The obdemo package contains a shell script that builds the rest of the
system and loads demonstration data (for Boston, MA) into the system::

 $ src/openblock/obdemo/bin/bootstrap_demo.sh

Wait 10 minutes or so; a lot of output will scroll by.
If it finishes successfully, you should see a message like::

 Demo bootstrap succeeded!

Now you can start the server::

 $ export DJANGO_SETTINGS_MODULE=obdemo.settings
 $ django-admin.py runserver

If all goes well, you should be able to visit the demo site at:
http://localhost:8000 

(If you're curious how the bootstrap script worked, have a look at
the source of ``obdemo/bin/bootstrap_demo.sh`` and the underlying
Paver script in :doc:`packages/obadmin`.)


If you run into trouble
-----------------------

If you encounter problems, double check that you have the basic
:ref:`requirements` installed.

Then you can try doing the part that failed by hand, and then
re-running ``bootstrap_demo.sh``.

Anytime you re-run ``bootstrap_demo.sh``, eg. if
you've got your system so broken that you want to start from scratch,
you may consider wiping out your existing database by giving the ``-r``
option::

 $ src/openblock/obdemo/bin/bootstrap_demo.sh -r  # DANGEROUS!

Note that this will completely and permanently wipe out your openblock
database, so think twice!

Finally, be aware (again) that ``bootstrap_demo.sh`` may simply not
work on your system!  Try the :ref:`detailed_demo_instructions` below.


For more help, you can try the ebcode group:
http://groups.google.com/group/ebcode
or look for us in the #openblock IRC channel on irc.freenode.net.


.. _detailed_demo_instructions:

Step-By-Step Demo Installation
==============================

These instructions do basically the same things as the
:ref:`demo_quickstart` above, but manually.

Basic Setup
-----------

First, follow **all** the instructions in the :doc:`setup` document.

.. _pythonreqs:

Installing Python packages
--------------------------------------------------

If you followed the :doc:`setup` instructions properly,
you've already got a virtualenv ready.  Go into it and activate it,
if you haven't yet::

  $ cd path/to/your/virtualenv
  $ source bin/activate

Check out the OpenBlock software::

    $ mkdir -p src/
    $ git clone git://github.com/openplans/openblock.git src/openblock

``Pip`` can install OpenBlock and the rest of our Python dependencies with a few
commands::

  $ cd $VIRTUAL_ENV/src/openblock
  $ pip install -r ebpub/requirements.txt -e ebpub
  $ pip install -r ebdata/requirements.txt -e ebdata
  $ pip install -r obadmin/requirements.txt -e obadmin
  $ pip install -r obdemo/requirements.txt -e obdemo


(We don't install :doc:`packages/ebgeo` because we assume you're not going to
be generating and serving your own map tiles.)


Editing Settings
----------------

You'll want to edit the demo's django settings at this point,
or at least look at it to get an idea of what can be
configured.  There is also some :doc:`configuration documentation <configuration>`
you should look at.


obdemo doesn't come with a settings.py; it comes with a
``settings.py.in`` template that you can copy and edit::

    $ cd $VIRTUAL_ENV/src/openblock/obdemo/obdemo
    $ cp settings.py.in settings.py
    $ favorite_editor settings.py


At minimum, you should change the values of:

* PASSWORD_CREATE_SALT - this is used when users create a new account.
* PASSWORD_RESET_SALT - this is used when users reset their passwords.
* STAFF_COOKIE_VALUE - this is used for allowing staff members to see
  some parts of the site that other users cannot, such as :doc:`types
  of news items <schemas>` that you're still working on.

You'll also want to think about :ref:`base_layer_configs`.


Database Initialization
-----------------------

Create the (empty) database, and a postgres user for it, with these commands::

    $ sudo -u postgres createuser --createdb openblock
    $ sudo -u postgres createdb -U openblock --template template_postgis openblock

Now initialize your database tables::

    $ export DJANGO_SETTINGS_MODULE=obdemo.settings
    $ django-admin.py syncdb --migrate


This will also bootstrap the :doc:`Schemas (types of news items) <schemas>`
used by the demo.

Multiple databases?
~~~~~~~~~~~~~~~~~~~

Note that while Django supports using multiple databases for different
model data, OpenBlock does not. This is because we use `South
<http://pypi.python.org/pypi/South>`_ to automate :ref:`database
migrations <migrations>`, and as of this writing South does not work
properly with a multi-database configuration.


Starting the Test Server
------------------------

Run these commands to start the test server::

  $ export DJANGO_SETTINGS_MODULE=obdemo.settings
  $ django-admin.py runserver

then visit http://127.0.0.1:8000/ in your Web browser to see the site in action (with no data)

.. _demodata:

Loading Demo Data
-----------------

OpenBlock is pretty boring without data!  You'll want to load some
:ref:`geographic data <locations>` and some local news.  We've
included some example data for Boston, MA, and scraper scripts you can
use to start with if you don't have all of your local data on hand yet.

Set your DJANGO_SETTINGS_MODULE environment variable before you begin.
(If you are loading the data into a different project, set this
variable accordingly -- e.g. ``myblock.settings`` instead of
``obdemo.settings``)::

  $ export DJANGO_SETTINGS_MODULE=obdemo.settings

First you'll want to load Boston geographies. This will take several minutes::

  $ cd src/openblock
  $ obdemo/bin/import_boston_zips.sh
  $ obdemo/bin/import_boston_hoods.sh
  $ obdemo/bin/import_boston_blocks.sh

Then fetch some news from the web, this will take several minutes::

  $ obdemo/bin/import_boston_news.sh


For testing with random data you might also want to try
``obdemo/bin/random_news.py 10`` ...
where 10 is the number of random articles to generate.  You must
first have some blocks in the database; it will assign randomly
generated local news articles to randomly chosen blocks.

Next Steps
==========

Now that you have the demo running, you might want to add some more
:doc:`custom content types <schemas>` to it, and write some
:doc:`scraper scripts <scraper_tutorial>` to populate them.
