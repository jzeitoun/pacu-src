from datetime import datetime

from pacu.util.path import Path
from pacu.util.identity import path
from pacu.util.newtype.snode.node.base import BaseNode
from pacu.util.newtype.snode.abc.mapper import BaseMapper
from pacu.core.scanbox.mapper.mat import MatMapper

class InfoItem(BaseNode):
    mappers = BaseMapper.extend(icon='info circle', classes='disabled')
    def on_map(self, mapping):
        return dict(text=self.data)
class ItemNode(BaseNode):
    def on_map(self, mapping):
        name = self.data.name
        return dict(text=name, value=name)
class DirItem(ItemNode):
    mappers = BaseMapper.extend(icon='folder', classes='fs-dir')
    weight = 10
    checker = Path.is_dir
class SBXFileItem(ItemNode):
    mappers = BaseMapper.extend(icon='file', classes='fs-file')
    weight = 20
    checker = MatMapper.can_deal_with
class DirectoryScanForSBX(BaseNode):
    routes = (DirItem, SBXFileItem)
    sort_keys = ('weight',)
    checker = Path.is_dir
    InfoNode = InfoItem
    def unfold(self):
        return self.data.glob('*')
    def makeup(self, items):
        if items:
            dirs = len(self.context['DirItem'])
            files = len(self.context['SBXFileItem'])
            yield self.link_info_node('Directory: {}, File: {}'.format(dirs, files))
        else:
            yield self.link_info_node('No scanbox files is in this directory...')
class SBXMetaItem(BaseNode):
    mappers = BaseMapper.extend(icon='info circle', classes='disabled')
    def on_map(self, mapping):
        return dict(text=self.data)
class FileScanForSBX(BaseNode):
    InfoNode = SBXMetaItem
    checker = MatMapper.can_deal_with
    def nodes(self):
        self.context['actions'].append('select')
        mat = MatMapper(self.data) # is path
        ctime = datetime.fromtimestamp(self.data.lstat().st_ctime)
        for key, val in mat.props.items():
            yield self.link_info_node('{}: {}'.format(key, val))
        yield self.link_info_node(
            'created at: {!s}'.format(ctime))
        yield self.link(InfoItem,
            'Hit Enter key or click the check icon to select this resource...')
    def on_select(self):
        return dict(data=self.data.with_name(self.data.stem).str)

class FSGraph(BaseNode):
    InfoNode = InfoItem
    routes = (
        DirectoryScanForSBX,
        FileScanForSBX,
    )
    def unfold(self):
        yield Path(self.data)

# print FSGraph(sbxpath).render().to_json()
# qwe = FSGraph(sbxpath.joinpath('JZ5', 'JZ5_000_003.mat')).render().to_json()
# print qwe.render().to_json()
# print qwe.catch()
# print qwe
# qwe = FSGraph(sbxpath.joinpath('fake-error-data.mat')).render().to_json()
# jz5 = '/Volumes/Users/ht/tmp/pysbx-data/JZ5/JZ5_000_003'
# f = FileGroup(jz5)

from pacu.profile import manager

sbxroot = manager.instance('opt').scanbox_root

sbxpath = Path(sbxroot)
# sbxpath = Path('/Volumes/Users/ht/tmp/pysbx-data')

def get(req, anchor, *hops, **kwargs):
    action = kwargs.get('action')
    # dest = path.cwd.joinpath(*hops)
    dest = sbxpath.joinpath(*hops)
    try:
        graph = FSGraph(dest)
        return graph.action(action) if action else graph.render().to_json()
    except Exception as e:
        print e
        raise e

