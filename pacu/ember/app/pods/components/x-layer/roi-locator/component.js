import Ember from 'ember';
import computed from 'ember-computed-decorators';

function makePolygon(cx, cy, nSides) {
  const size = 16;
  const pts = [];
  pts.push({
    x: parseInt(cx + size * Math.cos(0)),
    y: parseInt(cy + size * Math.sin(0))
  });
  for (let i = 1; i <= nSides;i += 1) {
    pts.push({
      x: parseInt(cx + size * Math.cos(i * 2 * Math.PI / nSides)),
      y: parseInt(cy + size * Math.sin(i * 2 * Math.PI / nSides))
    });
  }
  return pts;
}

export default Ember.Component.extend({
  tagName: 'svg',
  x: null,
  y: null,
  mouseMove({offsetX, offsetY}) {
    this.set('x', offsetX);
    this.set('y', offsetY);
  },
  click() {
    const polygon = this.get('polygon');
    this.get('workspace').appendROI({ polygon }).save();
  },
  @computed('x', 'y') pointAvailable(x, y) { return x && y; },
  @computed('x', 'y') polygon(x, y) {
    return makePolygon(x, y, 8);
  }
});
