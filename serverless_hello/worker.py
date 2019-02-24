import json
import os

from .s3 import get_object_from_s3, put_object_into_s3
from .worker_support import eval_expression


WORK_BUCKET = os.environ['WORK_BUCKET']
PROC_BUCKET = os.environ['PROC_BUCKET']
RES_BUCKET = os.environ['RES_BUCKET']


def start_work(event, context):
    """ starts work on a series of tasks;
    each line in an input file becomes a task, 
    a file of its own in a separate bucket
    """

    in_work_s3_object = get_object_from_s3(WORK_BUCKET, 'work.json')
    ops_bulk = in_work_s3_object['Body'].read().decode('utf-8')
    ops = json.loads(ops_bulk)['ops']

    for op in ops:
        put_object_into_s3(PROC_BUCKET, f"{op['name']}.work" , op['op'])

    body = {
        "message": ops,
        "input": event,
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
    }

    return response


def compute(event, context):
    """ computes the outcome of a work task, stores the outcome in a bucket
    """

    ev_key = event['Records'][0]['s3']['object']['key']
    to_eval_obj = get_object_from_s3(PROC_BUCKET, ev_key)
    to_eval = to_eval_obj['Body'].read().decode('utf-8')
    res = eval_expression(to_eval)
    put_object_into_s3(RES_BUCKET, f"{ev_key}.res", res)


