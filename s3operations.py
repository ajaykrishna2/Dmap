#Impoerted Required Moules
from flask import Flask,request
#Flask Restex Framework
from flask_restx import Api,Resource
import configparser
import os
import boto3
configuartion_path = os.path.dirname(os.path.abspath(__file__)) + "/config/config.ini"
print(configuartion_path)

config = configparser.ConfigParser()
config.read(configuartion_path);
aws_access_key = config['Aws_Credential']['s3_access_key'];
aws_secret_key = config['Aws_Credential']['s3_secret_key'];
bucket_region  = config['Aws_Credential']['bucket_region'];
bucket_name = config['Aws_Credential']['bucket_name'];

#Here we are creating a Flask App object
app = Flask(__name__);
#Here we are creating Api object imported from Restex Framework
api  = Api(app);



#This a class which is inheriting Resource Class

class s3_CRUD_operation(Resource):
    @classmethod
    def get(cls):
        try:
            session = boto3.Session(aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key,region_name=bucket_region);
            s3 = session.resource('s3')
            list_of_files = []
            my_bucket = s3.Bucket(bucket_name)
            for file in my_bucket.objects.all():
                list_of_files.append(file.key)
            return {'msg':list_of_files,'status':200}
        except Exception as e:
            return {'msg':"Unable to connect with s3",'status':500}
    @classmethod
    def post(cls):
        try:
            data = request.get_json();
            local_filename = data['local_filename'];
            aws_filename= data['aws_filename'];
            s3 = boto3.client('s3', aws_access_key_id=aws_access_key,
                              aws_secret_access_key=aws_secret_key,
                              region_name=bucket_region);
            s3.upload_file(local_filename, bucket_name, aws_filename)
            return {'msg':"file upload successful",'status':200}

        except Exception as e:
            return {'msg': "Unable to upload file to s3", 'status': 500}

    @classmethod
    def delete(cls):
        try:
            data = request.get_json();
            aws_filename = data['aws_filename'];
            session = boto3.Session(aws_access_key_id=aws_access_key,
                                    aws_secret_access_key=aws_secret_key,
                                    region_name=bucket_region);
            s3 = session.resource('s3')
            file = s3.Object(bucket_name,aws_filename)
            file.delete()
            return {'msg':"file deleted successfully",'status':200}

        except Exception as e:
            return {'msg': "Unable to delete file from s3", 'status': 500}

    @classmethod
    def put(cls):
        try:
            data = request.get_json();
            new_filename = data['new_filename'];
            aws_filename = data['aws_filename'];
            s3 = boto3.resource('s3')
            s3.Object(bucket_name, new_filename).copy_from(CopySource=bucket_name+"/"+aws_filename)
            s3.Object(bucket_name, aws_filename).delete()
            return {'msg':"file renamed successfully",'status':200}

        except Exception as e:
            return {'msg': "Unable to rename the file in s3", 'status': 500}


class s3_download_operation(Resource):
    @classmethod
    def post(cls):
        try:
            data = request.get_json();
            aws_filename = data['aws_filename']
            local_filename = data['local_filename'];
            s3 = boto3.client('s3', aws_access_key_id=aws_access_key,
                              aws_secret_access_key=aws_secret_key,
                              region_name=bucket_region);
            s3.download_file(bucket_name, aws_filename, local_filename)

            return {'msg': "file downloaded successfully", 'status': 200}

        except Exception as e:
            return {'msg': "Unable to download file from s3", 'status': 500}


api.add_resource(s3_download_operation,"/s3-download");





api.add_resource(s3_CRUD_operation,"/s3-operations");

if __name__ == "__main__":
    app.run(port=6001, debug=True)


