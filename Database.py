import csv
import os
from Tamagotchi import Tamagotchi
from google.cloud import storage
from pathlib import Path

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'GoogleCloud_SecurityKey.json'

storage_client = storage.Client()

"""
Uploading Tamagotchi file
"""


def set_Tamagotchi(client_id, instance : Tamagotchi):
    try:
        info = [str(instance.name),
                str(instance.age),
                str(instance.birthTime),
                str(instance.hunger),
                str(instance.happy),
                str(instance.hygiene),
                str(instance.image),
                str(instance.timeFed),
                str(instance.timePet),
                str(instance.timeClean),
                str(instance.state)]

        with open(r'.\instance.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(info)
        bucket = storage_client.get_bucket('tomohachi')
        blob = bucket.blob(client_id + '.csv')
        blob.upload_from_filename(r'.\instance.csv')
        os.remove(r'.\instance.csv')
        return True
    except Exception as e:
        print(e)
        return False


"""
Downloading Tamagotchi
"""


def get_Tamagotchi(client_id):
    try:
        bucket = storage_client.get_bucket('tomohachi')
        blob = bucket.blob(client_id + '.csv')
        with open(r'.\instance.csv', 'wb') as f:
            storage_client.download_blob_to_file(blob, f)

        with open(r'.\instance.csv') as f:
            reader = csv.reader(f)
            info = []
            info = next(reader)
        os.remove(r'.\instance.csv')
        instance = Tamagotchi("placeholder")
        instance.update(info[0],
                        int(float(info[1])),
                        float(info[2]),
                        int(float(info[3])),
                        int(float(info[4])),
                        int(float(info[5])),
                        Path(info[6]),
                        float(info[7]),
                        float(info[8]),
                        float(info[9]),
                        info[10])

        return instance
    except Exception as e:
        print(e)
        return Tamagotchi("Error")