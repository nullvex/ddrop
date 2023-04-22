import os
import struct
import secrets
import pyAesCrypt
import tarfile
import zipfile
import tarfile
import shutil
import ntpath
from datetime import datetime


class utils:
    def encrypt_file(self, password , in_filename, out_filename=None, chunksize=64*1024):
        """Encrypts a file using AES 256."""
        #Detect the type of file both on its face and inside of an archive
        file_type = utils.detect_file_type(self, in_filename)
        #Determine Filename and root path
        root_path, filename = ntpath.split(in_filename)
        # Getting the current date and time
        dt = datetime.now()
        # getting the timestamp
        ts = datetime.timestamp(dt)

        if not out_filename:
            out_filename = "%s.%s.tar.gz.enc" % (in_filename,ts)

        if file_type == 'directory' :
            #Set tarball filename
            tarname = "%s.%s.tar" % (filename, ts)
            #Set Path of Tarball to be
            tarpath = "%s/%s" % (root_path,tarname)
            #Create Tarball
            tarball = utils.make_tarfile(self, tarpath, in_filename)
            #Set Path of Encrypted Tarball to be
            outpath = "%s/%s" % (root_path, tarpath)
            #Encrypt Tarball
            pyAesCrypt.encryptFile(root_path, out_filename, password)
            print("Payload File: ", out_filename)

        elif file_type == 'non_archive_file' :
            #mkdir of same name as file in same target dir
            directory = utils.make_directory(self, ts, in_filename)
            #Create target Filename
            target_filename = "%s/%s" % (directory, filename)
            #Copy non_archive_file into newly created directory
            shutil.copyfile(in_filename, target_filename)
            tarname = "%s.tar" % (out_filename)
            tarball = utils.make_tarfile(self, tarname, directory)
            pyAesCrypt.encryptFile(tarname, out_filename, password)
            print("Payload File: ", out_filename)
            #clean up unencrypted tarball
            utils.delete_object(self, tarname)
            #clean up unencrypted directory
            utils.delete_object(self, directory)

        return out_filename


    def decrypt_file(self, password, in_filename, out_filename=None, chunksize=24*1024):
        """Decrypts a file using AES 512."""
        if not out_filename:
            out_filename = "%s.decrypted.tar" % ( in_filename )

        pyAesCrypt.decryptFile(in_filename , out_filename, password)

        return out_filename

    def make_tarfile(self, output_filename, source_dir):
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

    def make_directory(self, ts, file_path):
        directory_name = "%s_%s" % (file_path, ts)
        os.mkdir(directory_name)

        print("directory_name: ", directory_name)
        return directory_name

    def detect_file_type(self, source):
        if tarfile.is_tarfile(source):
            f = tarfile.open(source)
            for info in f:
                if info.isdir():
                    file_type = 'tar_directory'
                elif info.isfile():
                    file_type = 'tar_file'
                else:
                    file_type = 'tar_unknown'
                print('{} is a {}'.format(info.name, file_type))


        elif zipfile.is_zipfile(source):
            f = zipfile.ZipFile(source)
            for name in f.namelist():
                if name.endswith('/'):
                    file_type = "zip_directory"
                else:
                    file_type = "zip_file"
                print('{} is a {}'.format(name, 'zip_directory' if name.endswith('/') else 'zip_file'))

        elif os.path.isdir(source):
            file_type = "directory"

        else:
            print('{} is not an accepted archive file'.format(source))
            file_type="non_archive_file"

        print("Returned File Type: ", file_type)
        return file_type

    def delete_object(self, source):
        if os.path.isdir(source):
            deleted_file = shutil.rmtree(source)
        else:
            deleted_file = os.remove(source)
        return deleted_file
