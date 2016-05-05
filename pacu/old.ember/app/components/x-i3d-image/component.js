import Ember from 'ember';

export default Ember.Component.extend({
  contrast: 1.0,
  brightness: 1.0,
  setup: function() {
    window.asd = this;
    const session = this.getAttr('session');
    session.onbinary((buf) => {
      this.set('currentBuffer', buf);
    });
    session.access('dimension', 'max_index').then(([dimension, max_index]) => {
      this.setProperties({dimension, max_index});
      this.requestFrame(0);
    });
  }.on('didInsertElement'),
  updateFrame: function() {
    const index = parseInt(this.get('curIndex'));
    this.requestFrame(index);
  }.observes('curIndex'),
  requestFrame: function(index) {
    const self = this;
    const session = this.getAttr('session');
    if (self.get('framebusy')) {
      self.set('staledFrame', index); return;
    } else {
      session.invokeAsBinary('request_frame', index).gate(
      'framebusy').then(function() {
        const staledFrame = self.get('staledFrame');
        if (Ember.isPresent(staledFrame)) {
          self.set('staledFrame', null);
          self.requestFrame(staledFrame);
        }
      });
    }
  },
  currentROIs: function() { return []; }.property(),
  meanOfcROIs: Ember.computed.mapBy('currentROIs', 'mean'),
  actions: {
    mmXY(src) {
      // const dest = Ember.isEmpty(src[src.length-1]) ? src.slice(0, -1) : src;
      // return {
      //   minX: d3.min(dest, line => d3.min(line, (o, i) => i)),
      //   minY: d3.min(dest, line => d3.min(line, o => o)),
      //   maxX: d3.max(dest, line => d3.max(line, (o, i) => i)),
      //   maxY: d3.max(dest, line => d3.max(line, o => o))
      // };
    },
    createROI(x, y) {
      // const rois = this.get('currentROIs');
      // const roi = Ember.Object.create({
      //   x1: x, y1:y, x2:x, y2:y, mean: [], active: false
      // });
      // return rois.pushObject(roi);
    },
    activateROI(cur) {
      // for (let roi of this.get('currentROIs')) {
      //   if (Em.isEqual(cur, roi)) {
      //     roi.set('active', true);
      //     this.set('currentROI', roi);
      //   } else {
      //     roi.set('active', false);
      //   }
      // }
    },
    deactivateROI(roi) {
      // roi.set('active', false);
      // this.set('currentROI', null);
    },
    refreshROI(roi) {
      // const self = this;
      // const src = this.getAttr('src');
      // const qs = encodeURI(`?src=${src}`);
      // console.log('refROI with', src);
      // var xhr = new XMLHttpRequest();
      // xhr.open('GET', `/api/ping/${roi.x1}/${roi.x2}/${roi.y1}/${roi.y2}${qs}`, true);
      // xhr.responseType = 'arraybuffer';
      // xhr.onload = function(e) {
      //   try {
      //     const arr = new Float32Array(this.response);
      //     roi.set('mean', arr);
      //   } catch (e) {
      //     self.send('destroyROI', roi)
      //   }
      // };
      // xhr.onerror = function(e) { console.log(e); };
      // xhr.onprogress = function(e) {
      //   console.log('on progress!', e);
      //   console.log('length computable?', e.lengthComputable);
      //   console.log(e.loaded, e.total);
      // };
      // xhr.send();
    },
    destroyROI(roi) {
      // this.send('deactivateROI', roi);
      // this.get('currentROIs').removeObject(roi);
    },
  }
});
