import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'svg',
  classNames: ['roi-canvas'],
  widthBinding: 'mmw.width',
  heightBinding: 'mmw.height',
  activeBinding: 'mmw.active',
  attributeBindings: ['width', 'height'],
  @computed('elementId') svg(eid) {
    return d3.select('#' + eid);
  },
  initContainer: function() {
    this.set('objects', Ember.A());
  }.on('init'),
  mouseDown({offsetX, offsetY}) {
    const roi = this.get('objects').pushObject({
      x2: offsetX, y2: offsetY,
      x1: offsetX, y1: offsetY, temp: true});
    this.$().on('mousemove', this.onDrawROI.bind(this, roi));
    Ember.$(document).one('mouseup', this.didDrawROI.bind(this, roi));
  },
  onDrawROI(roi, {offsetX, offsetY}) {
    Ember.setProperties(roi, {
      x2: offsetX,
      y2: offsetY
    });
  },
  didDrawROI(roi) {
    this.$().off('mousemove');
    Ember.set(roi, 'temp', false);
  }
});
