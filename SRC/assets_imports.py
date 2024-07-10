import json
from settings import *

with open(get_path_actual("assets" + ".json")) as i:
    assets = json.load(i)


