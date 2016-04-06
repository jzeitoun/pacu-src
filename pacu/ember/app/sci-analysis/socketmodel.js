import Ember from 'ember';
import computed from 'ember-computed-decorators';
import ROI from 'pacu/components/x-layer/roi/roi';

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
  @computed() rois() { return []; },
  @computed('rois.@each.active') curROI(rois) {
    const cur = rois.findBy('active');
    window.cur = cur;
    return cur;
  },
  @computed('sfrequencies', 'sfrequency_index') curSF(sfs, index) {
    if (Ember.isNone(sfs)) { return; }
    return sfs[index];
  },
  @computed(
    'main_response', 'curROI.responses', 'curROI.busy', 'sfrequency_index'
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
  @computed('channel') img(ch) { return Image.create(ch); },
  @computed('roiFetching') socketStatusClass(rf) {
    const stat = rf ? 'active' : '';
    return new Ember.Handlebars.SafeString(stat);
  },
  initialize(route) {
    // window.qwe = this;
    this.mirror(
      'main_response', 'channel', 'sfrequencies',
      'sfrequency_index', 'sog_initial_guess'
    ).then((x) => {
      this.requestFrame(0);
    }).then(() => {
      this.invoke('session.roi.values').then(rois => {
        const news = this.get('rois').setObjects(
          rois.map(roi => ROI.create(roi).notifyPropertyChange('polygon'))
        );
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
    this.requestFrame(this.get('img.curIndex'));
  }.observes('img.curIndex')
});
