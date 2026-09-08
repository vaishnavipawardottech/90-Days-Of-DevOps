import yaml

with open('server.yml', 'r') as file:
    try:
        print(yaml.safe_load(file))
    except yaml.YAMLERROR as exc:
        print(exc)