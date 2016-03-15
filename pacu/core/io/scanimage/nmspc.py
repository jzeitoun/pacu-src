import cPickle as pickle

class HybridNamespace(dict):
    @classmethod
    def from_path(cls, path):
        self = cls()
        self.path = path
        self.peak()
        return self
    def __repr__(self):
        return '{}({}, {})'.format(type(self).__name__,
            super(HybridNamespace, self).__repr__(), repr(vars(self)))
    def save(self):
        with open(self.path.str, 'w') as f:
            pickle.dump(self, f)
        return self
    def load(self):
        with open(self.path.str, 'r') as f:
            self.update(pickle.load(f))
        return self
    def peak(self):
        try:
            self.load()
        except:
            pass
    def purge(self):
        self.clear()
        return self
    @property
    def has_data(self):
        return self.path.is_file()
    def create(self):
        if self.has_data:
            raise Exception('Namespace `{}` already exists.'.format(self.path.stem))
        self.save()
    def remove(self):
        if not self.has_data:
            raise Exception('Namespace `{}` does not exists.'.format(self.path.stem))
        self.path.unlink()
    def __delitem__(self, key):
        super(HybridNamespace, self).__delitem__(key)
        self.save()
    def __setitem__(self, key, val):
        super(HybridNamespace, self).__setitem__(key, val)
        self.save()
    def update(self, *args, **kwargs):
        super(HybridNamespace, self).update(*args, **kwargs)
        self.save()
    def setdefault(self, *args, **kwargs):
        rv = super(HybridNamespace, self).setdefault(*args, **kwargs)
        self.save()
        return rv
    def pop(self, key, default=None):
        rv = super(HybridNamespace, self).pop(key, default)
        self.save()
        return rv
