import Ember from 'ember';

export default Ember.Object.extend({
  initialExpand(x, y) {
    this.set('polygon.1.x', x);
    this.set('polygon.2.x', x);
    this.set('polygon.2.y', y);
    this.set('polygon.3.y', y);
  }
}).reopenClass({
  fromPoint: function(x, y) {
    return this.create({
      polygon: [{x, y}, {x, y}, {x, y}, {x, y}]
    });
  }
});
