from ddrop.utils import *
from cement import Controller, ex
from time import strftime
from os.path import exists
from tinydb import Query

class Archive(Controller):
    class Meta:
        label = 'archive'
        stacked_type = 'nested'
        stacked_on = 'base'

    #List Archives Locally Registered
    @ex(help='list archives')
    def list(self):
        data = {}
        data['archives'] = self.app.db.all()
        self.app.render(data, 'archives/list.jinja2')

    #Get Local Archive DB Details
    @ex(
        help = 'get archive details',
        arguments=[
            ( ['archive_id'],
             {'help': 'id of archive in local list',
              'action': 'store' } )
        ]
    )
    def get(self):
        data = {}
        print("ID: %s" % (self.app.pargs.archive_id))
        data['archives'] = self.app.db.all()
        print(data)
        result = data['archives'][0][0].encrypted_file
        print("Data: %s" % (result))
        #self.app.render(data, 'archives/record.jinja2')

    @ex(
        help='create an archive',
        arguments=[
            ( ['archive_name'],
              {'help': 'archive_name',
               'action': 'store' } ),
            ( ['-p', '--password'],
             {'help': 'a unique password',
              'action': 'store',
              'dest': 'password',
              'required': True
             } ),
            ( ['-f', '--file'],
             {'help': 'the file to encrypt',
              'action': 'store',
              'required': True,
              'dest': 'file_name' } )
        ],
    )
    def create(self):
        archive_name = self.app.pargs.archive_name
        password = self.app.pargs.password
        file_name = self.app.pargs.file_name
        now = strftime("%Y%m%d%H%M%S")
        self.app.log.info('creating  archive: %s' % archive_name)
        encrypted_file_name = utils.encrypt_file(self, password, file_name)

        archive = {
            'timestamp': now,
            'state': 'pending',
            'archive_name': archive_name,
            'encrypted_file': encrypted_file_name,
        }

        self.app.db.insert(archive)

    @ex(
        help='decrypt an archive',
        arguments=[
            ( ['-p', '--password'],
             {'help': 'a unique key',
              'dest': 'password' } ),
            ( ['-f', '--file'],
             {'help': 'the file to encrypt',
              'dest': 'file_name',
              'required': False } ),
            ( ['-e', '--extract'],
             {'help': 'extract tarball after decryption',
              'dest': 'extract' } )
        ],
    )
    def decrypt(self):
        if not self.app.pargs.file_name:
            Archive.list(self)
            archive_id = input("Enter Archive ID: ")
            file_name = Archive(archive_id).encrypted_file_name
            print("File to be decrypted: %s) % (file_name)")
        if not self.app.pargs.password:
            password = input("Enter Archive Password: ")

        password = self.app.pargs.password
        file_name = self.app.pargs.file_name
        extract = self.app.pargs.extract
        now = strftime("%Y%m%d%H%M%S")
        self.app.log.info('decrypting archive')
        decrypted_file_name = utils.decrypt_file(self, password, file_name, self.app.pargs.extract)
        archive = {
            'timestamp': now,
            'state': 'pending',
        }

    @ex(
        help='update an existing archive',
        arguments=[
            ( ['archive_id'],
              {'help': ' archive database id',
               'action': 'store' } ),
            ( ['--archive_name'],
              {'help': ' archive name',
               'action': 'store' ,
               'dest': 'archive_name' } ),
        ],
    )
    def update(self):
        id = int(self.app.pargs.archive_id)
        archive_name = self.app.pargs.archive_name
        now = strftime("%Y-%m-%d %H:%M:%S")
        self.app.log.info('updating archive: %s - %s' % (id, archive_name))

        archive = {
            'timestamp': now,
            'archive_name': archive_name,
        }

        self.app.db.update(archive, doc_ids=[id])

    @ex(
        help='delete an archive',
        arguments=[
            ( ['archive_id'],
              {'help': ' archive database id',
              'action': 'store' } ),
        ],
    )
    def delete(self):
        """ Deletes Record and associated archive files"""
        #fetch the id of the record in tinydb
        id = int(self.app.pargs.archive_id)
        #fetch the record from tinydb
        record = self.app.db.get(doc_id=id)
        #Detect the presence of a file path in the record
        if hasattr(record,'encrypted_file'):
            #Detect actual file on filesystem
            if exists(record['encrypted_file']):
                #Delete the File
                delete_file = utils.delete_object(self, record['encrypted_file'])
                #Log Deletion of File
                self.app.log.info('deleting file: %s' % record['encrypted_file'])
        #Remove record from TinyDB
        self.app.db.remove(doc_ids=[id])
        #Log Deletion of Archive in tinydb
        self.app.log.info('deleting archive id: %s' % id)
    def upload(self):
        """ Uploads the archive to a target cloud storage bucket """
        from google.cloud import storage


