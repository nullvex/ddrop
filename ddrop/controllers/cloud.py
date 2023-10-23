from ddrop.utils import *
from cement import Controller, ex
from time import strftime
from os.path import exists
from tinydb import Query

class Cloud(Controller):
    class Meta:
        label = 'cloud'
        stacked_type = 'nested'
        stacked_on = 'base'

    #List Clouds Locally Registered
    @ex(help='list clouds')
    def list(self):
        data = {}
        data['clouds'] = self.app.db.all()
        self.app.render(data, 'clouds/list.jinja2')

    #Get Local Cloud DB Details
    @ex(
        help = 'get cloud details',
        arguments=[
            ( ['bucket_id'],
             {'help': 'id of bucket in local list',
              'action': 'store' } )
        ]
    )
    def get(self):
        data = {}
        print("ID: %s" % (self.app.pargs.cloud_id))
        data['clouds'] = self.app.db.clouds.all()
        print(data)
        result = data['clouds'][0][0].encrypted_file
        print("Data: %s" % (result))
        #self.app.render(data, 'clouds/record.jinja2')

    @ex(
        help='create a cloud',
        arguments=[
            ( ['cloud_name'],
             {'help': 'cloud_name: gcp, aws',
               'action': 'store' } ),
            ( ['-j', '--service-account-json'],
             {'help': 'the service account json',
              'action': 'store',
              'dest': 'sa_file',
              'required': False
             } ),
            ( ['-b', '--bucket'],
             {'help': 'the target bucket',
              'action': 'store',
              'dest': 'bucket_id',
              'required': True
             } ),
            ( ['-i', '--key-id'],
             {'help': 'the key id value',
              'action': 'store',
              'dest': 'key_id',
              'required': True
             } ),
            ( ['-s', '--key-secret'],
             {'help': 'the secret key',
              'action': 'store',
              'required': True,
              'dest': 'secret_key' } )
        ],
    )
    def create(self):
        cloud_name = self.app.pargs.cloud_name
        bucket = self.app.pargs.bucket_id
        key_id = self.app.pargs.key_id
        secret_key = self.app.pargs.secret_key
        now = strftime("%Y%m%d%H%M%S")
        self.app.log.info('creating cloud: %s' % cloud_name)

        cloud = {
            'timestamp': now,
            'state': 'pending',
            'cloud_name': cloud_name,
            'bucket_id': bucket_id,
            'key_id': key_id,
            'secret_key': secret_key,
        }

        cloud_table = self.app.db.table('cloud')
        cloud_table.insert(cloud)
        self.app.db.insert(cloud)

    @ex(
        help='delete a cloud',
        arguments=[
            ( ['cloud_id'],
              {'help': ' cloud database id',
              'action': 'store' } ),
        ],
    )
    def delete(self):
        """ Deletes Record and associated cloud files"""
        #fetch the id of the record in tinydb
        id = int(self.app.pargs.bucket_id)
        #fetch the record from tinydb
        record = self.app.db.get(doc_id=id)
        #Remove record from TinyDB
        self.app.db.remove(doc_ids=[id])
        #Log Deletion of Cloud in tinydb
        self.app.log.info('deleting cloud id: %s' % id)

