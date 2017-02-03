import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'circle',
  attributeBindings: ['cx', 'cy'],
  cx: Ember.computed.alias('point.x'),
  cy: Ember.computed.alias('point.y')
}).reopenClass({
  positionalParams: ['point']
});
