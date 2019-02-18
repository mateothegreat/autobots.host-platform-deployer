import json
import subprocess

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [+] Received %r" % body)

    j = json.loads(body)

    uuid = j['payload']['uuid']
    repo = j['payload']['gitUrl']
    envs = j['payload']['environments']

    channel.queue_declare(queue=uuid, durable=True)
    channel.basic_publish(exchange='', routing_key=uuid, body='Received deployment request...')

    f = open('.env', 'w+')

    for i in range(len(envs)):

        print(envs[i]['name'])

        if len(envs[i]['name']) > 0 and len(envs[i]['value']) > 0:
            f.write(envs[i]['name'] + '=' + envs[i]['value'] + "\n")

    channel.basic_publish(exchange='', routing_key=uuid, body='Building docker image...')

    result = subprocess.run(['docker',
                             'build',
                             '--build-arg',
                             'REPO_URL=' + repo,
                             '-t',
                             'gcr.io/matthewdavis-devops/' + uuid + ':1',
                             '-f',
                             'Dockerfile.NODE_11_9_0_ALPINE',
                             '.'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    channel.basic_publish(exchange='', routing_key=uuid, body=result.stdout)

    channel.basic_publish(exchange='', routing_key=uuid, body='Uploading docker image...')

    result = subprocess.run(['docker',
                             'push',
                             'gcr.io/matthewdavis-devops/' + uuid + ':1'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    channel.basic_publish(exchange='', routing_key=uuid, body=result.stdout)

    channel.basic_publish(exchange='', routing_key=uuid, body='Deploying docker image...')

    subprocess.run(['make',
                    'delete',
                    'IMAGE=gcr.io/matthewdavis-devops/' + uuid + ':1',
                    'APP=' + uuid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    result = subprocess.run(['make',
                             'install',
                             'IMAGE=gcr.io/matthewdavis-devops/' + uuid + ':1',
                             'APP=' + uuid],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    channel.basic_publish(exchange='', routing_key=uuid, body=result.stdout)

    print(result.stdout)
    print(result.stderr)


# ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='autobots-queue-specific')

channel.start_consuming()
