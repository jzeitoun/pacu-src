from collections import namedtuple

import numpy as np

reserved = {'_items', '_names', '_namedtuple', 'items'}
reserved_attr_error = Exception(
    'Some of fields used reserved keywords. ({})'.format(', '.join(reserved))
)

class ZeroDimensionArrayView(object):
    def __init__(self, array):
        self._items = array.item()
        self._names = array.dtype.names
        if reserved & set(self._names):
            raise reserved_attr_error
        NTV = namedtuple('Contents', self._names)
        self._namedtuple = NTV(*[
            ZeroDimensionArrayView(item)
            if isinstance(item, np.ndarray) and item.shape == () else item
            for item in self._items
        ])
    def __dir__(self):
        return list(self._names) + list(reserved)
    def __getattr__(self, attr):
        return getattr(self._namedtuple, attr)
    def __iter__(self):
        return iter(
            (key, list(val) if isinstance(val, ZeroDimensionArrayView) else str(val))
            for key, val in self._namedtuple._asdict().items()
        )
    def items(self):
        return {
            key: (val.items() if isinstance(val, ZeroDimensionArrayView) else str(val))
            for key, val in self._namedtuple._asdict().items()
        }
