import Ember from 'ember';
import computed from 'ember-computed-decorators';
import ROI from 'pacu/components/x-layer/roi/roi';
import FilterModal from 'pacu/components/x-trj-analysis/filter/modal';

const Image = Ember.Object.extend({
  buffer: null,
  curIndex: 0,
  @computed('depth') maxIndex(d) {
    return d - 1;
  },
});

export default Ember.Object.extend({
  cmapNames: ['jet', 'gray', 'hot', 'hsv'],
  access(...fields) { return this.get('wsx').access(...fields); },
  mirror(...fields) { return this.get('wsx').mirrorTo(this, ...fields); },
  invoke(func, ...args) { return this.get('wsx').invoke(func, ...args); },
  @computed() rois() { return []; },
  @computed('rois.@each.active') curROI(rois) {
    return rois.findBy('active');
  },
  @computed(
    'main_response', 'curROI.response', 'curROI.busy'
  ) response(main, cur, busy) {
    if (busy) { return; }
    return cur || main;
  },
  @computed('channel') img(ch) { return Image.create(ch); },
  @computed('filter', 'velocity_stat') filterModal(filter, vstat) {
    return FilterModal.create(filter, {velocity: vstat});
  },
  @computed('img.curIndex', 'alog') curLog(i, log) {
    if (Ember.isNone(log)) { return; }
    return log.get(i);
  },
  @computed('img.curIndex', 'main_response') curActivity(i, resp) {
    if (Ember.isNone(resp)) { return 0; }
    return (resp.trace[i]/65536) * 100;
  },
  @computed('roiFetching') socketStatusClass(rf) {
    const stat = rf ? 'active' : '';
    return new Ember.Handlebars.SafeString(stat);
  },
  initialize(route) {
    this.mirror(
      'main_response', 'channel', 'alog', 'as_record', 'velocity_stat'
    ).then(() => {
      this.requestFrame(0);
    }).then(() => {
      this.invoke('session.opt.get', 'filter').then(filter => {
        const f = filter || {};
        if (Ember.isPresent(f.filterName) && f.filterName != 'none') {
          route.toast.info(`You are opening a 
            filtered image session. (${f.filterName})`);
        }
        f.model = this;
        f.route = route;
        this.set('filter', f);
      });
      this.invoke('session.roi.values').then(rois => {
        this.get('rois').setObjects(
          rois.map(roi => ROI.create(roi).notifyPropertyChange('polygon'))
        );
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
  }.observes('img.curIndex'),
  zContainerDimension: { height: 0 }
});
