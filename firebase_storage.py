from google.cloud import storage
client = storage.Client.from_service_account_json('key.txt')
bucket = client.get_bucket('pimirror-91ef6.appspot.com')

def getFileList():
    fileList = []
    for blob in bucket.list_blobs():
        fileList.append(blob.name) # blob.name: name of the file
        
    return fileList

def downloadFile(filename):
    bucket.blob(filename).download_to_filename(filename)

def uploadFile(filename):
    bucket.blob(filename).upload_from_filename(filename)

def deleteFile(filename):
    bucket.blob(filename).delete()