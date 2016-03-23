import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'ui inverted segment',
}).reopenClass({
  positionalParams: ['roi']
});
