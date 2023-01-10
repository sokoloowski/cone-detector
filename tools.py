from matplotlib.patches import Rectangle
import os, json


if os.path.exists('config/localconfig.py'):
    from config import localconfig as config
else:
    from config import config

def get_class(id):
    with open(os.path.join(config.BB_DATASET_PATH, 'meta.json')) as f:
        cone_classes = json.load(f)['classes']
    if id == 'all':
        return cone_classes
    return [x for x in filter(lambda x: x['id'] == id, cone_classes)][0]

def draw_bounding_box(object):
    pos = object['points']['exterior']
    w = pos[1][0] - pos[0][0]
    h = pos[1][1] - pos[0][1]
    obj_class = get_class(object['classId'])
    return Rectangle((pos[0][0], pos[0][1]), w, h, linewidth=1, edgecolor=obj_class['color'], facecolor='none')
