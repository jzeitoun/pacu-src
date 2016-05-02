from pacu.util.path import Path
from pacu.dep.json import best as json

raw_json = Path.here('all.json').read()
features = json.loads(raw_json)
