import Ember from 'ember';
import computed from 'ember-computed-decorators';

const ROI = Ember.Object.extend(Em.Copyable, {
  @computed() invalidated() { return true; },
  invalidate() {
    return this.setProperties({invalidated: true, active: false});
  },
  initialExpand(x, y) {
    this.set('polygon.1.x', x);
    this.set('polygon.2.x', x);
    this.set('polygon.2.y', y);
    this.set('polygon.3.y', y);
  },
  copy() {
    return ROI.create({
      active: this.active,
      busy: this.busy,
      id: this.id,
      invalidated: this.get('invalidated'),
      polygon: this.polygon.map(point => { return {
        x: point.x,
        y: point.y
      }; })
    });
  },
  derive() {
    const newroi = this.copy();
    this.setProperties({
      active: null,
      busy: null,
      id: +(new Date()),
      invalidated: true,
    });
    return newroi;
  }
}).reopenClass({
  fromPoint: function(x, y) {
    return this.create({
      polygon: [{x, y}, {x, y}, {x, y}, {x, y}],
      id: +(new Date())
    });
  },
  validate: function(roi) {
    return this.create(roi, {invalidated: Ember.isNone(roi.response)});
  }
});

export default ROI;
