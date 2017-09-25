import Ember from 'ember';
import computed from 'ember-computed-decorators';

const Image = Ember.Object.extend({
  buffer: null,
  curIndex: 0,
  @computed('depth') maxIndex(d) {
    return d - 1;
  },
});

export default Ember.Object.extend({
  access(...fields) { return this.get('wsx').access(...fields); },
  mirror(...fields) { return this.get('wsx').mirrorTo(this, ...fields); },
  invoke(func, ...args) { return this.get('wsx').invoke(func, ...args); },
  @computed('channelDimension') img(ch) { return Image.create(ch); },
  initialize(route, workspace) {
    // window.qwe = this;
    this.set('store', route.store);
    this.mirror('channel.dimension', 'ephys');
    if (Ember.isEmpty(workspace.get('rois'))) {
      route.toast.info(`Hey buddy, you have no ROIs in this workspace. 
        How about drawing some?`);
    }
  },
  requestFrame(index) {
    return this.get('wsx').invokeAsBinary(
        'channel.request_frame', parseInt(index)).then(buffer => {
      this.set('img.buffer', buffer);
    });
  },
  indexChanged: function() {
    this.requestFrame(this.get('img.curIndex'));
  }.observes('img.curIndex'),
  @computed() mainCanvasDimension() {
    return { height: 0 };
  },
  colorMapChanged: function() {
    const cmap = this.get('colorMap').toJSON();
    this.invoke('channel.update_colormap',
      cmap.basename, cmap.xmid1, cmap.ymid1, cmap.xmid2, cmap.ymid2
    ).then((/*data*/) => {
      this.indexChanged();
    });
  }.observes('colorMap.{basename,xmid1,ymid1,xmid2,ymid2}'),
});
