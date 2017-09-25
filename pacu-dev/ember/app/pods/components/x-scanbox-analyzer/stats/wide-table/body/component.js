import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'tbody',
  classNames: 'center aligned',
  @computed('condition.sfrequencies') subRows(sfreqs=[]) {
    return sfreqs;
  },
});
