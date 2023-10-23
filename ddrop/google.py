from google.cloud import storage

class GoogleStorageUploader:
    def __init__(self, project_id, bucket_name):
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.client = storage.Client(project=self.project_id)

    def upload_file(self, local_file_path, remote_file_name):
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(remote_file_name)
        blob.upload_from_filename(local_file_path)
        print(f"File {local_file_path} uploaded to {self.bucket_name}/{remote_file_name}")

# Usage example
#uploader = GoogleStorageUploader(project_id='your-project-id', bucket_name='your-bucket-name')
#uploader.upload_file('local_file.txt', 'remote_file.txt')

