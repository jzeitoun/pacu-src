import Ember from 'ember';
import computed from 'ember-computed-decorators';
import ROI from 'pacu/pods/components/x-layer/roi/roi';
// import FilterModal from 'pacu/components/x-trj-analysis/filter/modal';
// @on('didInsertElement')
// setupEditable() {
//   let options = {
//     placeholder: this.get('placeholder'),
//     emptytext:   this.get('emptytext'),
//     value:       this.get('value'),
//     success:     (res, value) => this.sendAction('setValue', value)
//   }

const Image = Ember.Object.extend({
  buffer: null,
  curIndex: 0,
  @computed('depth') maxIndex(d) {
    return d - 1;
  },
});

export default Ember.Object.extend({
//  cmapNames: ['jet', 'gray', 'hot', 'hsv'],
  access(...fields) { return this.get('wsx').access(...fields); },
  mirror(...fields) { return this.get('wsx').mirrorTo(this, ...fields); },
  invoke(func, ...args) { return this.get('wsx').invoke(func, ...args); },
//   @computed('rois.@each.active') curROI(rois) {
//     return rois.findBy('active');
//   },
//   @computed(
//     'main_response', 'curROI.response', 'curROI.busy'
//   ) response(main, cur, busy) {
//     if (busy) { return; }
//     return cur || main;
//   },
  @computed('channelDimension') img(ch) { return Image.create(ch); },
//   @computed('filter', 'velocity_stat') filterModal(filter, vstat) {
//     return FilterModal.create(filter, {velocity: vstat});
//   },
//   @computed('img.curIndex', 'alog') curLog(i, log) {
//     if (Ember.isNone(log)) { return; }
//     return log.get(i);
//   },
//   @computed('img.curIndex', 'main_response') curActivity(i, resp) {
//     if (Ember.isNone(resp)) { return 0; }
//     return (resp.trace[i]/65536) * 100;
//   },
//   @computed('roiFetching') socketStatusClass(rf) {
//     const stat = rf ? 'active' : '';
//     return new Ember.Handlebars.SafeString(stat);
//   },
//qwe.get('session').relationships.rois[0].attributes.polygon[0]
//
//   @computed('workspace.relationships.rois') rois(rois=[]) {
//     return rois.map(roi => {
//       const traces = roi.relationships.traces.map(trace => {
//         return trace.attributes;
//       });
//       return ROI.create(
//         roi.attributes, {id: roi.id, npEnabled: false, traces}
//       ).notifyPropertyChange('polygon'); // for recomputing roi
//     });
//   },
  // @computed() traces() {
  //   return this.get('store').peekAll('trace').mapBy('array');
  // },
  initialize(route, workspace) {
    this.set('store', route.store);
    this.mirror('channel.dimension');
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
});
