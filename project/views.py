from . import app

import os
import boto3


@app.route("/")
def index():
    return "Hello, world!", 200


HITS_TABLE = os.environ['HITS_TABLE']
client = boto3.client('dynamodb')


@app.route("/hit", methods=["POST"])
def hit():
    sid = request.json.get('sid')  # id for the site
    path = request.json.get('path')
    hostname = request.json.get('hostname')
    referrer = request.json.get('referrer')
    resolution = request.json.get('resolution')
    timezone = request.json.get('timezone')
    referrer_param = request.json.get('referrer_param')  # utm_source or ref
    new_visit = request.json.get('new_visit')

    if not sid or not path or not hostname or not referrer or not resolution or not timezone
    or not referrer_param or not new_visit:
            return jsonify({'error': 'Missing details'}), 400

    resp = client.put_item(
        TableName=HITS_TABLE,
        Item={
            'sid': {'S': sid},
            'path': {'S': path},
            'hostname': {'S': hostname},
            'referrer': {'S': referrer},
            'resolution': {'S': resolution},
            'timezone': {'S': timezone},
            'referrer_param': {'S': referrer_param},
            'new_visit': {'S': new_visit}
        }
    )

    return jsonify({
        'sid': sid,
        'path': path,
        'hostname': hostname,
        'referrer': referrer,
        'resolution': resolution,
        'timezone': timezone,
        'referrer_param': referrer_param,
        'new_visit': new_visit
    })
