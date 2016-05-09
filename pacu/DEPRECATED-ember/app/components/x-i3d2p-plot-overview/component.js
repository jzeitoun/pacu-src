import Ember from 'ember';
import computed from 'ember-computed-decorators';
import d3 from 'd3';

export default Ember.Component.extend({
  tagName: 'canvas',
  width: 800,
  height: 200,
  attributeBindings: ['width', 'height'],
  @computed ctx() {
    return this.element.getContext('2d');
  },
  draw: function() {
    const src = this.getAttr('src');
    const width = this.get('width');
    const height = this.get('height');
    if (Ember.isNone(src)) { return; }

    const ctx = this.get('ctx');
    ctx.clearRect(0, 0, this.element.width, this.element.height);

    const scaleY = d3.scale.linear().range([0, height]).domain(d3.extent(src));
    const scaleX = d3.scale.linear().range([0, width]).domain([0, src.length]);

    ctx.beginPath();
    ctx.strokeStyle = '#0FF';
    ctx.lineWidth = 0.25;
    src.forEach(function(d, i) {
      ctx.lineTo(scaleX(i), scaleY(d));
    });
    ctx.stroke();
    ctx.closePath();

  }.observes('attrs.src')
});
