import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'table',
  classNames: `ui celled unstackable selectable
    inverted structured small compact table`,
  @computed('rois.[]') ttestNames(rois) {
    if (Ember.isEmpty(rois)) {
      return [];
    } else {
      const ttest = rois[0].get('sortedResponses.0.stats.ttest')
      if (ttest) {
        return ttest.mapBy('name');
      } else {
        return [];
      }
    }
  }
});
