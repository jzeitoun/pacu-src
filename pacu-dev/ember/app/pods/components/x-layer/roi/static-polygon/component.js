import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'polygon',
  attributeBindings: ['points', 'stroke'],
  @computed('polygon.@each.{x,y}') points(pg) {
    if (Ember.isNone(pg)) { return; }
    return pg.map(point => { return `${point.x},${point.y}`; }).join(' ');
  },
}).reopenClass({
  positionalParams: ['polygon']
})
