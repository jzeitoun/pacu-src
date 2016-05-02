import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'table',
  classNames: `ui celled unstackable selectable
    inverted structured small compact table`,
  debug: function() {window.asd = this;}.on('didInsertElement'),
  @computed('rois.[]') ttestNames(rois) {
    if (Ember.isEmpty(rois)) {
      return [];
    } else {
      return rois[0].get('sortedResponses.0.stats.ttest').mapBy('name');
    }
  }
});
