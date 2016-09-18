import Ember from 'ember';
import computed from 'ember-computed-decorators';
import ROI from 'pacu/pods/components/x-layer/roi/roi';
// import ColormapModal from 'pacu/components/x-sci-analysis/colormap';

const Image = Ember.Object.extend({
  buffer: null,
  curIndex: 0,
  @computed('depth') maxIndex(d) {
    return d - 1;
  },
});

export default Ember.Object.extend({
  xmid: 50,
  ymid: 50,
  cmap: 'jet',
  access(...fields) { return this.get('wsx').access(...fields); },
  mirror(...fields) { return this.get('wsx').mirrorTo(this, ...fields); },
  invoke(func, ...args) { return this.get('wsx').invoke(func, ...args); },
  @computed() logs() { return []; },
  @computed() rois() { return []; },
  @computed('rois.@each.active') curROI(rois) {
    const cur = rois.findBy('active');
    // window.cur = cur;
    return cur;
  },
  @computed('sfrequencies', 'sfrequencyIndex') curSF(sfs, index) {
    if (Ember.isNone(sfs)) { return; }
    return sfs[index];
  },
  // For each cell, if the ANOVA each p value is
  // less than 0.01 at the cell's peak SF it is responsive.
  // If it is greater than 0.01 at the cell's peak SF then
  // it is NOT responsive.
  @computed('rois.[]') responsiveROIs(rois) {
    return rois.filter(r => {
      // if ($.isEmptyObject(r.responses)) { return false; }
      try {
        return r.responses[r.sfreqfit.peak].stats.anova.p < 0.01;
      } catch (err) {
        console.log('exception at filtering responsive ROI', err);
        return false;
      }
    });
  },
  @computed('rois.[]') irresponsiveROIs(rois) {
    return rois.filter(r => {
      // if ($.isEmptyObject(r.responses)) { return false; }
      try {
        return r.responses[r.sfreqfit.peak].stats.anova.p >= 0.01;
      } catch (err) {
        console.log('exception at filtering irresponsive ROI', err);
        return false;
      }
    });
  },
  @computed(
    'mainResponse', 'curROI.responses', 'curROI.busy', 'sfrequencyIndex'
  ) response(main, cur, busy, sfreqIndex) {
    if (busy) { return; }
    if (Ember.isPresent(cur)) {
      const sfreq = this.get('sfrequencies')[sfreqIndex];
      return cur[sfreq];
    } else {
      return main;
    }
    return cur || main;
  },
  @computed('channel', 'channelNumber') img(ch) { return Image.create(ch); },
  @computed('roiFetching') socketStatusClass(rf) {
    const stat = rf ? 'active' : '';
    return Ember.String.htmlSafe(stat);
  },
  initialize(route) {
    window.SM = this;
    this.mirror(
      'main_response', 'channel',
      'channel_numbers', 'channel_number',
      'colormaps', 'colormap_index',
      'sfrequencies', 'sfrequency_index',
      'r_value',
      'sog_initial_guess'
    ).then((x) => {
      this.requestFrame(0);
    }).then(() => {
      this.addObserver('channelNumber', this.channelChanged);
      this.invoke('session.roi.values').then(rois => {
      // this.invoke('session.load_rois').then(rois => {
        const roiObjects = rois.map(roi => {
          const newroi = ROI.create(roi);
          newroi.set('guessParams', newroi.guess_params);
          return newroi.notifyPropertyChange('polygon');
        });
        window.rs = roiObjects;
        const news = this.get('rois').setObjects(roiObjects);
        // news[0].set('active', true);
        // this.set('sfrequency_index', 1);
        if (Ember.isEmpty(rois)) {
          route.toast.info(`Hey buddy, you have no ROIs in this session. 
            How about drawing some?`);
        }
      });
    });
  },
  requestFrame(index) {
    return this.get('wsx').invokeAsBinary(
        'channel.request_frame', parseInt(index)).then(buffer => {
      this.set('img.buffer', buffer);
    });
  },
  indexChanged: function() {
    const index = this.get('img.curIndex');
    this.get('rois').forEach(roi => roi.indexChanged(index));
    this.requestFrame(index);
  }.observes('img.curIndex'),
  channelChanged: function() {
    const num = this.get('channelNumber');
    this.invoke('set_channel', num);
    location.reload();
  }
});
