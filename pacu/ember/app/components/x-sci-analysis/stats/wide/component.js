import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'table',
  classNames: `ui celled unstackable selectable
    inverted structured small compact table`,
  debug: function() {window.asd = this;}.on('didInsertElement'),
  @computed('rois') items(rois) {
    console.log('sort...');
    return rois;
  },
}).reopenClass({
  positionalParams: ['rois']
});
