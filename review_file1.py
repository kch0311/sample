import boto3
import sys

def replay_copy(endpoint, access_key, secret_key):
  s3_client = boto3.client("s3", endpoint_url=endpoint, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

  response = s3_client.create_bucket(Bucket="replaycopy")
  print("[PUT BUCKET]", response)
  import pdb; pdb.set_trace();
  response = s3_client.put_object(Bucket="replaycopy", Key="objecta")
  print("[PUT OBJECT]", response)

  try:
    response = s3_client.copy_object(Bucket="replaycopy", Key="objecta", CopySource="")
    print("[COPY OBJECT]", response)
  except Exception as ec:
    print(ec)
    pass

replay_copy(endpoint=sys.argv[1], access_key=sys.argv[2], secret_key=sys.argv[3])
