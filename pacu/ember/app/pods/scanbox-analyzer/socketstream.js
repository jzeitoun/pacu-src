import Ember from 'ember';
import computed, { on } from 'ember-computed-decorators';

const Image = Ember.Object.extend({
  mpi: false,
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
  @computed('ch0Dimension') img(ch) { return Image.create(ch); },
  @on('init') initialize() {
    this.mirror('ch0.dimension', 'ch0.has_maxp');
  },
  requestFrame(index) {
    return this.get('wsx').invokeAsBinary(
        'ch0.request_frame', parseInt(index)).then(buffer => {
      this.set('img.buffer', buffer);
      this.set('img.mpi', false);
    });
  },
  indexChanged: function() {
    this.requestFrame(this.get('img.curIndex'));
  }.observes('img.curIndex'),
  @computed() mainCanvasDimension() {
    return { height: 0 };
  },
  overlayMPI() {
    this.get('wsx').invokeAsBinary('ch0.request_maxp').then(buffer => {
      this.set('img.buffer', buffer);
      this.set('img.mpi', true);
    });
  }
  // colorMapChanged: function() {
  //   const cmap = this.get('colorMap').toJSON();
  //   this.invoke('channel.update_colormap',
  //     cmap.basename, cmap.xmid1, cmap.ymid1, cmap.xmid2, cmap.ymid2
  //   ).then((data) => {
  //     this.indexChanged();
  //   });
  // }.observes('colorMap.{basename,xmid1,ymid1,xmid2,ymid2}'),
});
