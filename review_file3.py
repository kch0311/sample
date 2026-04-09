import boto3
from botocore.exceptions import ClientError

# --- Configuration ---
BUCKET_NAME = "new-kri1"
TAGS = [{"Key": "type", "Value": "log"}]   # tags you want to apply
PREFIX = ""                                # optional, e.g. "vgoot/1/172.234.239.206/"

args = {
    "access_key": "",
    "secret_key": "",
    "endpoint_url": "http://us-sea-3.linodeobjects.com",
}

# If using AWS S3:
session = boto3.Session(aws_access_key_id=args['access_key'], aws_secret_access_key=args['secret_key'])
s3 = session.resource('s3', endpoint_url=args['endpoint_url'])

# --- Apply tags ---
paginator = s3.meta.client.get_paginator("list_objects_v2")

for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=PREFIX):
    for obj in page.get("Contents", []):
        key = obj["Key"]
        try:
            s3.meta.client.put_object_tagging(
                Bucket=BUCKET_NAME,
                Key=key,
                Tagging={"TagSet": TAGS}
            )
            print(f"✅ Tagged: {key}")
        except ClientError as e:
            print(f"❌ Failed to tag {key}: {e}")


