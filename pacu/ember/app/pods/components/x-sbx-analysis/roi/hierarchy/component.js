import Ember from 'ember';
import computed from 'ember-computed-decorators';
import color from 'pacu/utils/color';

export default Ember.Component.extend({
  classNames: 'ui',
  @computed('colorIndex') colorStyle(ci) {
    return Ember.String.htmlSafe(`background-color: ${color.google20[ci]}`);
  }
});
