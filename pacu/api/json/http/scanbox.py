from pacu.profile import manager
from pacu.core.io.scanbox.impl import ScanboxIO

opt = manager.instance('opt')

def index_meta(directory):
    recording_paths = sorted(set(
        path.with_suffix('.io')
        for path in opt.scanbox_root.joinpath(directory).ls('*.sbx')
        if path.is_file()))
    recordings = map(ScanboxIO, recording_paths)
    metas = [r.meta for r in recordings]
    return dict(directory=directory, metas=metas)

def index_directory():
    directories = sorted(set(path.name
        for path in opt.scanbox_root.ls()
        if path.is_dir()))
    return dict(directories=directories)

def get_index(req, directory=None):
    return index_meta(directory) if directory else \
           index_directory()

def post_session(req, path, session): # session_name
    io = ScanboxIO(path)
    io.create_session(name=session)
    return io.meta

def delete_session(req, path, session_id):
    io = ScanboxIO(path)
    io.delete_session(session_id)
    return io.meta
