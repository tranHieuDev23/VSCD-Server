from random import randint
from time import time

CLASSES = set([
    'Không',
    'Một',
    'Hai',
    'Ba',
    'Bốn',
    'Năm',
    'Bảy',
    'Tám',
    'Chín',
    'Trái',
    'Phải',
    'Lên',
    'Xuống',
    'Tiến',
    'Lùi',
    'Có'
])

def generate_filename(uuid, ext):
    return str(uuid) + ":" + str(time()) + ":" + str(randint(0, 100000)) + '.' + ext

def generate_validation_id(uuid, id):
    return str(uuid) + ":" + str(time()) + ":" + str(id) + str(randint(0, 100000))
