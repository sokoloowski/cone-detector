# %%
import os
import json

# Load configuration
if os.path.exists('config/localconfig.py'):
    from config import localconfig as config
else:
    from config import config

# %%
max_objects = 0

# %%
if not os.path.exists(config.BB_OBJECTS):
    os.mkdir(config.BB_OBJECTS)

annot_paths = [f for f in os.listdir(config.BB_ANNOTATIONS)]
for path in annot_paths:
    with open(os.path.join(config.BB_ANNOTATIONS, path)) as f:
        annot = json.load(f)
    objects = []
    for o in annot['objects']:
        objects.append({'class': o['classTitle'],
                        'top_left': {'x': o['points']['exterior'][0][0],
                                     'y': o['points']['exterior'][0][1]},
                        'bottom_right': {'x': o['points']['exterior'][1][0],
                                         'y': o['points']['exterior'][1][1]}})

    if len(objects) > 10:
        continue

    max_objects = max(max_objects, len(objects))
    if len(objects) == 122:
        print(path)

    with open(os.path.join(config.BB_OBJECTS, path), 'w') as f:
        json.dump(objects, f) 

# %%
if not os.path.exists(config.BB_TARGET):
    os.mkdir(config.BB_TARGET)

annot_paths = [f for f in os.listdir(config.BB_OBJECTS)]
for path in annot_paths:
    with open(os.path.join(config.BB_OBJECTS, path)) as f:
        annot = json.load(f)
    
    target = [(None, None, None, None) for _ in range(10)]
    for i in range(len(annot)):
        target[i] = (annot[i]['top_left']['x'],
                     annot[i]['top_left']['y'],
                     annot[i]['bottom_right']['x'],
                     annot[i]['bottom_right']['y'])

    with open(os.path.join(config.BB_TARGET, path), 'w') as f:
        json.dump(target, f)


