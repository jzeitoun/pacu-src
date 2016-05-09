import Ember from 'ember';
import computed from 'ember-computed-decorators';
import ROI from '../components/x-layer/roi/roi';

export default Ember.Controller.extend({
  on_sse_print: function(msg, err) {
    console.log(`Backend: ${msg}`);
  },
  @computed() rois() { return []; },
  arrayWillChange: function(array, offset, removes, _) {
    for (let i=offset; i<offset+removes; i++) {
      this.send('deleteROI', array[i]);
    }
  },
  arrayDidChange: function(array, offset, _, adds) {
    for (let i=offset; i<offset+adds; i++) {
      this.send('upsertROI', array[i]);
    }
  },
  curROI: null,
  @computed('curROI', 'curROI.busy') curROINotBusy(roi, busy) {
    return Ember.isPresent(roi) && !busy;
  },
  curIndex: 0,
  actions: {
    currentSFrequencyEnumChange: function(_, index) {
      console.log(index);
    },
    deleteROI(roi) {
      if (Ember.isPresent(roi.rid)) {
        this.get('session').invoke('delete_roi', roi.rid);
      }
    },
    upsertROI(roi, ...fields) {
      this.get('session').invoke('upsert_roi', roi, ...fields).then(data => {
        roi.setProperties(data);
      });
    },
    readAllROI() {
      this.get('session').access('rois').then(rois => {
        const rs = rois.map(function(roi) { return ROI.create(roi); });
        this.get('rois').pushObjects(rs);
      });
    },
    fetchData(roi) {
      if (roi.get('busy')) { return; }
      roi.set('busy', true);
      this.get('session').invoke('fetch_roi_data', roi.rid).then(data => {
        debugger
      }).finally(() => {
        roi.set('busy', false);
      });
    }
  },
  refresh: function() {
    const session = this.get('session');
    session.invoke('condition.extract').then(condition => {
      this.set('condition', condition.attributes);
      // session.invoke('get_grand_trace').gate('busy').then(trace => {
      //   this.set('trace', trace);
      // });
      // session.invoke('get_current_sfrequency').then(value => {
      //   this.set('current_sfrequency', value);
      // });
      session.access('dimension').then(img => {
        this.set('img.depth', img.depth);
        this.set('img.width', img.width);
        this.set('img.height', img.height);
        this.requestFrame(0);
        this.send('readAllROI');
      });
    });
  }.observes('session'),
  cleanup: function(transition) {
    this.session.dnit();
    this.session = null;
    this.set('curIndex', null);
    this.set('current_sfrequency', null);
    this.get('rois').removeArrayObserver(this);
  },
  initialize: function() {
    // window.qwe = this;
    this.onBuf = this.set.bind(this, 'img.buffer');
    this.set('img', {width: 0, height: 0, depth: 0, buffer: null});
    this.get('rois').addArrayObserver(this);
  }.on('init'),
  @computed('img.depth') maxIndex(d) {
    return d - 1;
  },
  requestFrame: function(index) {
    const session = this.get('session');
    return session.invokeAsBinary('request_frame', parseInt(index)).then(this.onBuf);
  },
  indexChanged: function() {
    const index = this.get('curIndex');
    if (Ember.isNone(index)) return;
    this.requestFrame(parseInt(index));
  }.observes('curIndex'),
  // play() {
  //   if (this.playing) { return; }
  //   this.playing = true;
  //   const session = this.get('session');
  //   const run = () => {
  //     if (this.shouldStop) {
  //       this.playing = false;
  //       this.shouldStop = false;
  //     }
  //     session.invokeAsBinary(
  //       'request_frame', this.incrementProperty('curIndex')
  //     ).then(buf => {
  //       requestAnimationFrame(run);
  //       this.onBuf(buf);
  //     });
  //   };
  //   run();
  // },
  // stop() {
  //   if (!this.playing) { return; }
  //   this.shouldStop = true;
  // }
});
