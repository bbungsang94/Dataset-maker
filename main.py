import os
import json
from runner import REGISTRY as Runners
from labeler import REGISTRY as Labelers
from contents import REGISTRY as Models


def read_json(full_path=''):
    if '.json' not in full_path:
        full_path += '.json'
    with open(full_path, "r") as f:
        file = json.load(f)
    return file


def main(config):
    names = config['names']
    config['runner']['labeler'] = Labelers[names['labeler']](**config['labeler'])
    config['runner']['model'] = Models[names['model']](**config['model'])

    runner = Runners[names['runner']](**config['runner'])
    runner.loop()


if __name__ == "__main__":
    args = read_json(os.path.join('./config', 'args.json'))
    main(args)
