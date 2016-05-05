from pacu.profile import manager
from pacu.core.io.scanbox.impl import ScanboxIO

opt = manager.instance('opt')

def index_meta(directory):
    io_paths = sorted(set(
        path.with_suffix('.io')
        for path in opt.scanbox_root.joinpath(directory).ls('*.sbx')
        if path.is_file()))
    ios = map(ScanboxIO, io_paths)
    return dict(directory=directory, io_attrs_set=[r.attributes for r in ios])

def index_directory():
    directories = sorted(set(path.name
        for path in opt.scanbox_root.ls()
        if path.is_dir()))
    return dict(directories=directories)

def get_index(req, directory=None):
    return index_meta(directory) if directory else \
           index_directory()

# def post_workspace(req, path, session): # session_name
#     io = ScanboxIO(path)
#     # io.create_session(name=session)
#     return io.meta
# 
# def delete_workspace(req, path, session_id):
#     io = ScanboxIO(path)
#     wrg
#     # io.delete_session(session_id)
#     return io.meta
