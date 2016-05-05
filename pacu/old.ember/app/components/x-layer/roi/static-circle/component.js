import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'circle',
  attributeBindings: ['cx', 'cy'],
  cx: Ember.computed.alias('attrs.point.x'),
  cy: Ember.computed.alias('attrs.point.y'),
}).reopenClass({
  positionalParams: ['point']
});
