import Ember from 'ember';
import computed from 'ember-computed-decorators';
import d3 from 'd3';

export default Ember.Component.extend({
  socket: Ember.inject.service(),
  d3: Ember.inject.service(),
  initWS: function() {
    window.qwe = this;
    const src = this.getAttr('files');
    this.wsx = this.get('socket').create(
      this, 'pacu.core.svc.analysis.i3d', 'I3DAnalysisService', src
    ).then(() => {
      this.wsx.access('stack.shape').then(this.setShape).then(this.zeroFrame);
    });
  }.on('didInsertElement'),
  dnitWS: function() { this.wsx.dnit(); }.on('willDestroyElement'),
  setShape(shape) {
    ['Z', 'Y', 'X'].forEach((e, i) => {
      this.set(`stack${e}`, shape[i]);
    });
  },
  zeroFrame() {
    this.wsx.onbinary(this.setBuffer).invokeAsBinary('get_frame', 0);
  },
  setBuffer(buf) {
    this.set('currentBuffer', buf);
  },
  @computed('stackZ') maxIndex(z) {
    return (z || 1) - 1;
  },
  curIndex: 0, // and maxIndex is 0
  updateFrame: function() {
    const index = parseInt(this.get('curIndex'));
    this.wsx.invokeAsBinary('get_frame', index);
  }.observes('curIndex'),
  currentROIs: function() { return []; }.property(),
  meanOfcROIs: Ember.computed.mapBy('currentROIs', 'mean'),
  actions: {
    mmXY(src) {
      const dest = Ember.isEmpty(src[src.length-1]) ? src.slice(0, -1) : src;
      return {
        minX: d3.min(dest, line => d3.min(line, (o, i) => i)),
        minY: d3.min(dest, line => d3.min(line, o => o)),
        maxX: d3.max(dest, line => d3.max(line, (o, i) => i)),
        maxY: d3.max(dest, line => d3.max(line, o => o))
      };
    },
    hookROI(x, y) {
      const rois = this.get('currentROIs');
      const roi = Ember.Object.create({x1: x, y1:y, x2:x, y2:y, mean: []});
      return rois.pushObject(roi);
    },
    refreshROI(roi) {
      console.log('refROI');

      // this.wsx.invoke('get_mean', roi.x1, roi.x2, roi.y1, roi.y2).then((data) => {
      //   roi.set('mean', data);
      // });

      var xhr = new XMLHttpRequest();
      xhr.open('GET', `/api/ping/${roi.x1}/${roi.x2}/${roi.y1}/${roi.y2}`, true);
      xhr.responseType = 'arraybuffer';
      xhr.onload = function(e) {
        const arr = new Float32Array(this.response);
        roi.set('mean', arr);
      };
      xhr.onprogress = function(e) {
        console.log('on progress!', e);
        console.log('length computable?', e.lengthComputable);
        console.log(e.loaded, e.total);
      };
      xhr.send();
    },
    destroyROI(roi) {
      this.get('currentROIs').removeObject(roi);
    },
  }
});
