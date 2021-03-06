''' Command Line Interface for setting up Open Letters stores

'''

import os
import sys

import paste.script.command

class BaseCommand(paste.script.command.Command):
    parser = paste.script.command.Command.standard_parser(verbose=True)
    parser.add_option('-c', '--config', dest='config',
            default='development.ini', help='Config file to use (default: development.ini)')
    default_verbosity = 1
    group_name = 'openletters'

    def _load_config(self):
        from paste.deploy import appconfig
        from openletters.config.environment import load_environment
        if not self.options.config:
            msg = 'No config file supplied'
            raise self.BadCommand(msg)
        self.filename = os.path.abspath(self.options.config)
        conf = appconfig('config:' + self.filename)
        load_environment(conf.global_conf, conf.local_conf)

    def _setup_app(self):
        cmd = paste.script.appinstall.SetupCommand('setup-app') 
        cmd.run([self.filename]) 


class ManageDb(BaseCommand):
    '''Perform various tasks on the database.
    
    db create
    db clean
    db rebuild # clean and create
    # db upgrade [{version no.}] # Data migrate 
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 1

    def command(self):
        self._load_config()
        from openletters import model

        cmd = self.args[0]
        if cmd == 'create':
            model.repo.create_db()
        elif cmd == 'clean' or cmd == 'drop':
            model.repo.clean_db()
        elif cmd == 'rebuild':
            model.repo.rebuild_db()
        elif cmd == 'upgrade':
            if len(self.args) > 1:
                model.repo.upgrade_db(self.args[1])
            else:
                model.repo.upgrade_db()
        else:
            print 'Command %s not recognized' % cmd
            sys.exit(1)


class Fixtures(BaseCommand):
    '''Load (and remove) fixture data.

        setup: setup fixtures
        teardown: teardown the fixtures
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 1

    def command(self):
        self._load_config()
        action = self.args[0]
        if action == 'setup':
            self.setup()
        elif action == 'teardown':
            self.teardown()
    
    perm_url = u'http://openletters.org/letters/testing'

    @classmethod
    def setup(self):
        from openletters import model
        letter = model.Letter(volume=1, type=u'dickens',
                correspondent=u'Mr MaCready', perm_url=self.perm_url,
                letter_text=u'xxxxx', letter_date=u'6th August 1847')
        model.Session.add(letter)
        model.Session.commit()
        model.Session.remove()

    @classmethod
    def letter(self):
        '''Get the letter the fixtures create.'''
        from openletters import model
        letter = model.Session.query(model.Letter).\
                filter_by(perm_url=self.perm_url).one()
        return letter

    @classmethod
    def teardown(self):
        from openletters import model
        letters = model.Session.query(model.Letter
                ).filter_by(perm_url=self.perm_url).all()
        for l in letters:
            model.Session.delete(l)
        model.Session.commit()
        model.Session.remove()


class Load(BaseCommand):
    '''Load external data into domain model.

        dickens: Load Dickens data.
        
        endpoint: create the RDF/JSON/XML endpoints
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 1

    def command(self):
        self._load_config()
        cmd = self.args[0]
        if cmd == 'dickens':
            fileobj = 'openletters/docs/dickens_letters.xml'
            source_obj = 'openletters/docs/dickens_source.xml'
            book_obj = 'openletters/docs/dickens_texts.xml'
            location_obj = 'openletters/docs/dickens_places.xml'
            import openletters.command
            openletters.command.load_dickens_letters(fileobj)
            openletters.command.load_source(source_obj)
            openletters.command.load_texts(book_obj)
            openletters.command.load_locations(location_obj)

        elif cmd == 'endpoint':
            import openletters.command
            openletters.command.create_endpoint()
            
        else:
            print 'Action not recognized'


class Index(BaseCommand):
    ''' Index the letters for a Xapian powered search
    
       index dickens  - indexes the Dickens letters
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 1
    
    def command(self):
        self._load_config()
        cmd = self.args[0]
        
        if cmd == 'dickens':
            type = 'dickens'
            fileobj = 'openletters/docs/dickens_letters.xml'
            import openletters.command
            
            openletters.command.index_letters(self, type, fileobj)
        else:
            print 'Action not recognized'