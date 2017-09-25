import Ember from 'ember';
import computed from 'ember-computed-decorators';

/* global Uint8ClampedArray */

export default Ember.Component.extend({
  tagName: 'canvas',
  active: true,
  attributeBindings: ['width', 'height', 'style'],
  classNameBindings: ['active', 'attrs.staticPos'],
  @computed('contrast', 'brightness') style(c, b) {
    return `-webkit-filter: contrast(${c}) brightness(${b})`;
  },
  @computed('ctx', 'width', 'height') img(c, w, h) {
    if (Ember.isNone(w) || Ember.isNone(h)) { return; }
    return c.getImageData(0, 0, w, h);
  },
  @computed ctx() {
    return this.$()[0].getContext('2d');
    // or this.element.getContext('2d'); ?
  },
  bufferChanged: function() {
    var {img, ctx, buf} = this.getProperties('img', 'ctx', 'buf');
    if (Ember.isNone(img) || Ember.isNone(buf)) { return; }
    img.data.set(new Uint8ClampedArray(buf));
    ctx.putImageData(img, 0, 0);
  },
  registerObserver: function() {
    this.addObserver('buf', this.bufferChanged);
  }.on('didInsertElement')
});
