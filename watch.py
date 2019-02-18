# from kubernetes import client, config, watch
#
# # Configs can be set in Configuration class directly or using helper utility
# config.load_kube_config()
#
# v1 = client.CoreV1Api()
# count = 10
# w = watch.Watch()
# for event in w.stream(v1.read_namespaced_pod_log('f80770a4-3ea6-4223-abdd-4e32dd661980-96f7dc9c8-865j7', 'default'),
#                       _request_timeout=60):
#     print("Event: %s %s" % (event['type'], event['object'].metadata.name))
#     count -= 1
#     if not count:
#         w.stop()
#
# print("Ended.")
from __future__ import print_function

from pprint import pprint

import kubernetes.client
from kubernetes import config
from kubernetes.client.rest import ApiException

# Configure API key authorization: BearerToken
config.load_kube_config()

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['authorization'] = 'Bearer'

# create an instance of the API class
api_instance = kubernetes.client.CoreV1Api()
name = 'f80770a4-3ea6-4223-abdd-4e32dd661980-76d558bd9f-hzw5k'  # str | name of the Pod
namespace = 'default'  # str | object name and auth scope, such as for teams and projects
container = 'f80770a4-3ea6-4223-abdd-4e32dd661980'  # str | The container for which to stream logs. Defaults to only container if there is one container in the pod. (optional)
follow = True  # bool | Follow the log stream of the pod. Defaults to false. (optional)
limit_bytes = 56000  # int | If set, the number of bytes to read from the server before terminating the log output. This may not display a complete final line of logging, and may return slightly more or slightly less than the specified limit. (optional)
pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)
previous = False  # bool | Return previous terminated container logs. Defaults to false. (optional)
since_seconds = 56  # int | A relative time in seconds before the current time from which to show logs. If this value precedes the time a pod was started, only logs since the pod start will be returned. If this value is in the future, no logs will be returned. Only one of sinceSeconds or sinceTime may be specified. (optional)
tail_lines = 56  # int | If set, the number of lines from the end of the logs to show. If not specified, logs are shown from the creation of the container or sinceSeconds or sinceTime (optional)
timestamps = True  # bool | If true, add an RFC3339 or RFC3339Nano timestamp at the beginning of every line of log output. Defaults to false. (optional)

try:

    api_response = api_instance.read_namespaced_pod_log(name, namespace, container=container, follow=follow,
                                                        limit_bytes=limit_bytes, pretty=pretty, previous=previous,
                                                        since_seconds=since_seconds, tail_lines=tail_lines,
                                                        timestamps=timestamps)
    pprint(api_response)

except ApiException as e:

    print("Exception when calling CoreV1Api->read_namespaced_pod_log: %s\n" % e)
