import Ember from 'ember';

const ROI = Ember.Object.extend(Em.Copyable, {
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
      rid: this.rid,
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
      rid: null
    });
    return newroi;
  }
}).reopenClass({
  fromPoint: function(x, y) {
    return this.create({
      polygon: [{x, y}, {x, y}, {x, y}, {x, y}]
    });
  }
});

export default ROI;
