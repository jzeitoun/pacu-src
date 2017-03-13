import Ember from 'ember';
import computed from 'ember-computed-decorators';

function makePolygon(cx, cy, nSides, size=16) {
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
  hide: false,
  attributeBindings: 'style',
  @computed('hide') style(hide) {
    const visibility = hide ? 'hidden' : 'show';
    return `visibility: ${visibility}`;
  },
  mouseMove({offsetX, offsetY}) {
    this.set('x', offsetX);
    this.set('y', offsetY);
  },
  click() {
    const polygon = this.get('polygon');
    this.get('workspace').appendROI({ polygon }).save();
  },
  nSides: 8,
  size: 16,
  @computed('x', 'y') pointAvailable(x, y) { return x && y; },
  @computed('x', 'y', 'nSides', 'size') polygon(x, y, n, s) {
    return makePolygon(x, y, n, s);
  },
  didInsertElement(){
    Mousetrap.bind('esc', e => {
      const stream = this.get('stream');
      stream.indexChanged();
    });
    Mousetrap.bind('tab', e => {
      e.preventDefault();
      this.toggleProperty('hide');
    });
    Mousetrap.bind('up', e => {
      e.preventDefault();
      if (this.get('nSides') > 16) return;
      this.incrementProperty('nSides');
    });
    Mousetrap.bind('down', e => {
      e.preventDefault();
      if (this.get('nSides') < 4) return;
      this.decrementProperty('nSides');
    });
    Mousetrap.bind('right', e => {
      e.preventDefault();
      if (this.get('size') > 64) return;
      this.incrementProperty('size');
    });
    Mousetrap.bind('left', e => {
      e.preventDefault();
      if (this.get('size') < 4) return;
      this.decrementProperty('size');
    });
  },
  willDestroyElement(){
    Mousetrap.unbind('esc');
    Mousetrap.unbind('tab');
    Mousetrap.unbind('up');
    Mousetrap.unbind('down');
    Mousetrap.unbind('right');
    Mousetrap.unbind('left');
  }
});
