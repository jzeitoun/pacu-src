import Ember from 'ember';
import computed from 'ember-computed-decorators';
import ROI from '../components/x-layer/roi/roi';

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
    return rois.findBy('active');
  },
  @computed(
    'main_response', 'curROI.response', 'curROI.busy'
  ) response(main, cur, busy) {
    if (busy) { return; }
    return cur || main;
  },
  @computed('channel') img(ch) { return Image.create(ch); },
  @computed('roiFetching') socketStatusClass(rf) {
    const stat = rf ? 'active' : '';
    return new Ember.Handlebars.SafeString(stat);
  },
  initialize(route) {
    this.mirror('main_response', 'channel').then(() => {
      this.requestFrame(0);
    }).then(() => {
      this.invoke('session.search', 'roi').then(rois => {
        this.get('rois').setObjects(rois.map(roi => ROI.validate(roi)));
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