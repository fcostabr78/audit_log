import io, json, logging, oci
from datetime import datetime
from random import randint
from oci.object_storage.models import CreateBucketDetails
from fdk import response


compartment_id = 'ocid1.tenancy.oc1..aaaaaaaaqqzek25x6oc72fsf7pl5pxqipakzcual27u6db3njlq76p7jopna'

def save_log(signer, body, event_type):
    object_storage = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    namespace = object_storage.get_namespace().data
    my_data = json.dumps(body)
    bucket_name = event_type

    try:
        request = CreateBucketDetails()
        request.compartment_id = compartment_id
        request.name = bucket_name
        object_storage.create_bucket(namespace, request)
    except (Exception) as ex:
        logging.getLogger().info('error creating bucket: ' + str(ex))

    ts = str(datetime.utcnow().microsecond)
    object_name = 'log' + ts + str(randint(0, 10000)) + '_' + event_type
    object_storage.put_object(namespace, bucket_name, object_name, my_data)


def handler(ctx, data: io.BytesIO=None):
    event_type = "mockEventType"
    body = ""

    try:
        body = json.loads(data.getvalue())
        event_type = body["eventType"]
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))

    ts = str(datetime.utcnow())
    signer = oci.auth.signers.get_resource_principals_signer()
    resp = json.dumps({
        "UTC": "{0}".format(ts),
        "Event Type": "{0}".format(event_type), 
        "body": "{0}".format(body), 
        "URL context": ctx.RequestURL(), 
        "Header context": ctx.Headers()},
        indent = 4)
    save_log(signer, resp, event_type)
    return response.Response(
        ctx, response_data=resp, headers={"Content-Type": "application/json"}
    )
