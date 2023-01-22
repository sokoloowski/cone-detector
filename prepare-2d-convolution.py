# %%
import tensorflow as tf

print(tf.__version__)
print(tf.keras.__version__)

# %%
import os
if os.path.exists('config/localconfig.py'):
    from config import localconfig as config
else:
    from config import config

# %%
target_paths = os.listdir(config.BB_OBJECTS)

import random
random.shuffle(target_paths)

images, targets = [], []

# %%
size = len(target_paths)
import json

for i in range(size):
    with open(os.path.join(config.BB_OBJECTS, target_paths[i])) as f:
        cones = json.load(f)

    image = tf.keras.utils.load_img(os.path.join(config.BB_IMAGES, target_paths[i][:-5]))
    for cone in cones:
        I_cone = tf.image.crop_to_bounding_box(image,
                                               cone['top_left']['y'],
                                               cone['top_left']['x'],
                                               cone['bottom_right']['y'] - cone['top_left']['y'],
                                               cone['bottom_right']['x'] - cone['top_left']['x'])
        images.append(tf.keras.utils.img_to_array(I_cone))
        targets.append(cone['class'])

# %%
for i in range(len(images)):
    image = tf.keras.utils.array_to_img(images[i])
    image = image.resize((224, 224))
    images[i] = tf.keras.utils.img_to_array(image)

# %%
import pandas as pd

targets = pd.get_dummies(targets)

# %%
classes = targets.columns
targets = targets.values

# %%
with open("dataset.json", "w") as f:
    json.dump({'X': images,
               'y': targets,
               'classes': classes}, f)


