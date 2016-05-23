import Ember from 'ember';
import computed, { on } from 'ember-computed-decorators';
import interaction from 'pacu/utils/interaction';
import color from 'pacu/utils/color';

export default Ember.Component.extend({
  tagName: 'svg',
  classNameBindings: ['augKeyOn'],
  mouseDown(e) {
    const $target = this.parentView.$();
    return interaction.bindOnce.call(this, $target, e);
  },
  leaving(origin, offset, offsetY) {
    return this.get('layer.do')('appendModel', 'roi', {polygon: [
      {x: origin.x, y: origin.y},
      {x: offset.x, y: origin.y},
      {x: offset.x, y: offset.y},
      {x: origin.x, y: offset.y},
    ]});
  },
  movingWith(origin, offset, roi) {
    [['1.x', offset.x], ['2.x', offset.x],
     ['2.y', offset.y], ['3.y', offset.y]].forEach(([key, val]) => {
      roi.set(`polygon.${key}`, val);
    });
  },
  left(origin, offset, roi) { return roi.save(); },
  @on('didInsertElement') initialize() {
    Ember.$(document).on('keydown.roi-manager', ({altKey, metaKey}) => {
      this.set('augKeyOn', altKey || metaKey);
    });
    Ember.$(document).on('keyup.roi-manager', () => {
      this.set('augKeyOn', false);
    });
  },
  @on('willDestroyElement') dinitialize() {
    Ember.$(document).off('keydown.roi-manager');
    Ember.$(document).off('keyup.roi-manager');
  },
  @computed('rois.[]') coloredROIs(rois) {
    return rois.map((r, i) => {
      return {roi: r, color: color.getGoogle20(i)};
    });
  }
});
