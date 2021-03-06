A project which tries to define the social networks that can be defined from
letters written in the nineteenth century. Currently the project focuses on
Charles Dickens but this will be expanded as new datasets are created. 

Project home page (wiki): http://wiki.okfn.org/p/Open_Letters

Installation and Setup
======================

You will need to have python, mercurial, setuptools, virtualenv and pip to
install ``openletters`` (all other dependencies will be automatically installed
using pip)::

    # check out the code to openletters directory
    hg clone https://knowledgeforge.net/letters/hg openletters

    # move into the directory
    cd openletters

    # now install it to virtualenv at ../pyenv-openletters using pip
    pip -E ../pyenv-openletters install -r pip-requirements.txt


Make a config file as follows::

    paster make-config openletters development.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.


Using the Command Line Tools
============================

Our command line tools have been created as `paster commands` (and found in
openletters/cli.py). To get a list do::

    paster -h

And look at commands in openletters section (some of other commands may be
useful to). To get more info on a given command do::

    paster {command} -h

.. _paster commands: http://pythonpaste.org/script/developer.html

