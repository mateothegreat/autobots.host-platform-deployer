import datetime
import json
import subprocess
import time

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [+] Received %r" % body)

    j = json.loads(body)

    uuid = j['payload']['uuid']
    repo = j['payload']['gitUrl']
    envs = j['payload']['environments']
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    image = 'gcr.io/matthewdavis-devops/' + uuid + ':' + timestamp

    channel.queue_declare(queue=uuid, durable=True)
    channel.basic_publish(exchange='', routing_key=uuid, body='Received deployment request...')

    make_env_args = ['VERSION=' + timestamp]

    for i in range(len(envs)):

        print(envs[i]['name'])

        if len(envs[i]['name']) > 0 and len(envs[i]['value']) > 0:
            make_env_args.append('ENV_' + str(i + 1) + '_NAME=' + envs[i]['name'])
            make_env_args.append('ENV_' + str(i + 1) + '_VALUE=' + envs[i]['value'])

    channel.basic_publish(exchange='', routing_key=uuid, body='Building docker image...')

    result = subprocess.run(['docker',
                             'build',
                             '--build-arg',
                             'REPO_URL=' + repo,
                             '-t',
                             image,
                             '-f',
                             'Dockerfile.NODE_11_9_0_ALPINE',
                             '.'])

    # channel.basic_publish(exchange='', routing_key=uuid, body=result.stdout)

    channel.basic_publish(exchange='', routing_key=uuid, body='Uploading docker image...')

    result = subprocess.run(['docker',
                             'push',
                             image])

    # channel.basic_publish(exchange='', routing_key=uuid, body=result.stdout)
    channel.basic_publish(exchange='', routing_key=uuid, body='Deploying docker image...')

    subprocess.run(['make',
                    'delete',
                    'APP=' + uuid])

    arr = ['make',
           'install',
           'IMAGE=' + image,
           'APP=' + uuid] + make_env_args

    print(arr)

    result = subprocess.run(arr)

    print(result.returncode)

    if result.returncode == 0:
        channel.basic_publish(exchange='', routing_key=uuid, body='Bot deployed!')
    else:
        channel.basic_publish(exchange='', routing_key=uuid, body='Bot could not be deployed :*(')

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='autobots-queue-specific')

channel.start_consuming()
