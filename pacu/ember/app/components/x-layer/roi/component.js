import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.reopenClass({
  positionalParams: ['roi']
}).extend({
  tagName: 'g',
  @computed('roi.polygon.@each.{x,y}') points(pgs) {
    if (Ember.isNone(pgs)) { return; }
    return pgs.map(point => { return `${point.x},${point.y}`; }).join(' ');
  },
  circles: Ember.computed.alias('roi.polygon')
});
