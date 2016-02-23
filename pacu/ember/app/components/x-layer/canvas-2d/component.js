import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'canvas',
  @computed('ctx', 'width', 'height') img(c, w, h) {
    if (Ember.isNone(w) || Ember.isNone(h)) { return; }
    this.element.width = w;
    this.element.height = h;
    return c.getImageData(0, 0, w, h);
  },
  @computed ctx() {
    return this.element.getContext('2d');
  },
  bufferChanged: function() {
    var {img, ctx, buffer} = this.getProperties('img', 'ctx', 'buffer');
    if (Ember.isNone(img) || Ember.isNone(buffer)) { return; }
    img.data.set(new Uint8ClampedArray(buffer));
    ctx.putImageData(img, 0, 0);
  }.observes('buffer'),
});
