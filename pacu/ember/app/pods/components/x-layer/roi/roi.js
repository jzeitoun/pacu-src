import Ember from 'ember';
import computed from 'ember-computed-decorators';
import Centroid from 'pacu/pods/components/x-layer/roi/centroid';
import Neuropil from 'pacu/pods/components/x-layer/roi/neuropil';
import Trajectory from 'pacu/pods/components/x-layer/roi/trajectory';

const ROI = Ember.Object.extend(Ember.Copyable, Centroid, Neuropil, Trajectory, {
  @computed() invalidated() { return true; },
  @computed() responses() { return {}; },
  @computed() traces() { return []; },
  @computed('responses') responseCount(resp) {
    return Object.keys(resp).length;
  },
  @computed('responseCount') responseCountPlusOne(c) {
    return c + 1;
  },
  @computed('responses') sortedResponses(resp) {
    return Object.keys(resp).sort().map(k => resp[k]);
  },
  invalidate: function() {
    return this.setProperties({
      invalidated: true,
      active: false,
      bootstrap_sf: null,
    });
  },
  initialExpand(x, y) {
    this.set('polygon.1.x', x);
    this.set('polygon.2.x', x);
    this.set('polygon.2.y', y);
    this.set('polygon.3.y', y);
  },
  copy() {
    const newROI = ROI.create();
    const keys = Object.keys(this).removeObjects(['toString']);
    for (let key of keys) {
      newROI.set(key, Ember.copy(this[key], true));
    }
    return newROI;
  },
  derive() {
    // newroi will stay at same location as if it was the original.
    // And `this` will be acting like a newly copied roi.
    const newroi = this.copy();
    delete this.id;
    return newroi;
  }
}).reopenClass({
  fromPoint: function(x, y) {
    return this.create({
      polygon: [{x, y}, {x, y}, {x, y}, {x, y}],
    });
  }
});

export default ROI;
