# Generate Grafana dashboard (JSON) from list of instances

import os.path
import json

INSTANCE_DASHBOARD_FOLDER = '../grafana/instance-dashboards'

with open('instances.txt', 'r') as f:
    instances = [i[:-1] for i in f.readlines()]

with open('../grafana/standard-dashboard.json', 'r') as f:
    dashboard = json.load(f)

# TODO: check if instance mapper exists and use this if so

if not os.path.isdir(INSTANCE_DASHBOARD_FOLDER):
    os.mkdir(INSTANCE_DASHBOARD_FOLDER)
for instance in instances:
    dashboard['title'] = instance
    for panel in dashboard['panels']:
        panel['title'] = instance
        for target in panel['targets']:
            target['expr'] = target['expr'].replace('$$INSTANCE$$', instance)
    with open('../grafana/instance-dashboards/%s.json' % instance, 'w') as f:
        json.dump(dashboard, f)
