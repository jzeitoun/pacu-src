import ujson

from pacu.util.path import Path

raw_json = Path.here('all.json').read()
features = ujson.loads(raw_json)
