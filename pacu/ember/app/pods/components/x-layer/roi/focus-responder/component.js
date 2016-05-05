import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'a',
  classNames: 'focus-responder',
  initialize: function() {
    this.$().attr('link:href', '#');
  }.on('didInsertElement')
});
