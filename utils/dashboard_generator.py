# Generate Grafana dashboard (JSON) from list of instances

import os.path
import json

INSTANCE_DASHBOARD_FOLDER = '../grafana/instance-dashboards'
INSTANCE_MAP = 'instance_map.txt'

with open('instances.txt', 'r') as f:
    instances = [i[:-1] for i in f.readlines()]

with open('../grafana/standard-dashboard.json', 'r') as f:
    dashboard = json.load(f)

if os.path.isfile(INSTANCE_MAP):
    instance_map = dict()
    with open(INSTANCE_MAP) as f:
        for l in f.readlines():
            instance, name = l.split()
            instance_map.update({instance: name})

if not os.path.isdir(INSTANCE_DASHBOARD_FOLDER):
    os.mkdir(INSTANCE_DASHBOARD_FOLDER)
for instance in instances:
    dashboard['title'] = instance_map[instance] if instance_map else instance
    for panel in dashboard['panels']:
        for target in panel['targets']:
            target['expr'] = target['expr'].replace('INSTANCE', instance)
    with open('../grafana/instance-dashboards/%s.json' % instance, 'w') as f:
        json.dump(dashboard, f)
