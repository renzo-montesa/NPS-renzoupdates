import json
import config


UPLOAD_FOLDER = config.UPLOAD_DIR


def write_json_to_file(data):
    with open(UPLOAD_FOLDER + 'data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
