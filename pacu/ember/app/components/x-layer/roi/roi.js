import Ember from 'ember';
import computed from 'ember-computed-decorators';
import Centroid from 'pacu/components/x-layer/roi/centroid';
import Neuropil from 'pacu/components/x-layer/roi/neuropil';

const ROI = Ember.Object.extend(Em.Copyable, Centroid, Neuropil, {
  @computed() invalidated() { return true; },
  invalidate: function() {
    return this.setProperties({invalidated: true, active: false});
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
