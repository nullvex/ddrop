from ddrop.utils import *
from cement import Controller, ex
from time import strftime

class Archive(Controller):
    class Meta:
        label = 'archive'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(help='list archives')
    def list(self):
        data = {}
        data['archives'] = self.app.db.all()
        self.app.render(data, 'archives/list.jinja2')

    @ex(
        help='create an archive',
        arguments=[
            ( ['archive_name'],
              {'help': 'archive_name',
               'action': 'store' } ),
            ( ['-p', '--password'],
             {'help': 'a unique password',
              'action': 'store',
              'dest': 'password' } ),
            ( ['-f', '--file'],
             {'help': 'the file to encrypt',
              'action': 'store',
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
            ( ['archive_name'],
              {'help': 'archive name',
               'action': 'store' } ),
            ( ['-p', '--password'],
             {'help': 'a unique key',
              'dest': 'password' } ),
            ( ['-f', '--file'],
             {'help': 'the file to encrypt',
              'dest': 'file_name' } )
        ],
    )
    def decrypt(self):
        archive_name = self.app.pargs.archive_name
        password = self.app.pargs.password
        file_name = self.app.pargs.file_name
        now = strftime("%Y%m%d%H%M%S")
        self.app.log.info('creating  archive: %s' % archive_name)
        decrypted_file_name = utils.decrypt_file(self, password, file_name)
        print(decrypted_file_name)

        archive = {
            'timestamp': now,
            'state': 'pending',
            'archive_name': archive_name,
        }

        self.app.db.insert(archive)

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
        id = int(self.app.pargs.archive_id)
        self.app.log.info('deleting  archive id: %s' % id)
        self.app.db.remove(doc_ids=[id])
