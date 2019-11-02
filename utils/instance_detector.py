import flask


app = flask.Flask(__name__)
instances = []


def persist_instances(instances: list) -> None:
    with open('instances.txt', 'w') as f:
        f.writelines([i + '\n' for i in instances])


@app.route('/metrics/job/climate/instance/' + '<instance>', methods=['POST'])
def get_instance(instance):
    if instance not in instances:
        instances.append(instance)
    persist_instances(instances)
    return '', 204


app.run(
    debug=True,
    host='0.0.0.0',
    port=9091
)
