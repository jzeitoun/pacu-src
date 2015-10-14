import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'canvas',
  widthBinding: 'mmw.width',
  heightBinding: 'mmw.height',
  activeBinding: 'mmw.active',
  attributeBindings: ['width', 'height'],
  classNameBindings: ['active'],
  @computed('ctx', 'width', 'height') img(c, w, h) {
    if (Ember.isNone(w) || Ember.isNone(h)) { return; }
    return c.getImageData(0, 0, w, h);
  },
  @computed ctx() {
    return this.$()[0].getContext('2d');
  },
  bufferChanged: function() {
    var data = this.get('mmw.currentBuffer');
    var {img, ctx} = this.getProperties('img', 'ctx');
    if (Ember.isNone(img) || Ember.isNone(data)) { return; }
    var prev = new Uint32Array(img.data.buffer);
    var next = new Uint32Array(data);
    var len = prev.length;
    while(len--) { prev[len] = next[len]; }
    ctx.putImageData(img, 0, 0);
  },
  registerObserver: function() {
    console.log('RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRCA');
    this.addObserver('mmw.currentBuffer', this.bufferChanged);
  }.on('didInsertElement')
});
