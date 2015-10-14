import Ember from 'ember';
import computed from 'ember-computed-decorators';
import d3 from 'd3';

const ViewBox = Ember.Object.extend({
  top: 10,
  right: 0,
  bottom: 25,
  left: 30,
  WIDTH: null,
  HEIGHT: null,
  @computed('WIDTH', 'left', 'right') width(w, l, r) {
    return w-l-r;
  },
  @computed('HEIGHT', 'top', 'bottom') height(h, t, b) {
    return h-t-b;
  },
  @computed('WIDTH', 'HEIGHT', 'left', 'top') attr(w, h, l, t) {
    return `${-l} ${-t} ${w} ${h}`;
  },
});

export default Ember.Component.extend({
  tagName: 'svg',
  interpolate: 'linear',
  @computed('attrs.width', 'attrs.height') vb(WIDTH=256, HEIGHT=256) {
    return ViewBox.create({WIDTH, HEIGHT});
  },
  @computed('elementId') clipPathId(id) {
    return `clip-path-${id}`;
  },
  @computed('clipPathId') clipPathRef(id) {
    return `url(.${window.location.pathname}#${id})`;
  },
  attributeBindings: 'vb.width:width vb.height:height vb.attr:viewBox'.w(),
  @computed('src.[]') dtype(src) {
    if (src.hasOwnProperty('length')) {
      if (src.length > 0 && src[0].hasOwnProperty('length')) {
        return 2;
      } else { return 1; }
    } else { return 0; }
  },
  @computed('src.[]') mmXY(src) {
    if (Ember.isPresent(this.attrs.onmmXY)) {
      return this.attrs.onmmXY(src);
    } else {
      return {
        minX: d3.min(src, line => d3.min(line, o => o.x)),
        minY: d3.min(src, line => d3.min(line, o => o.y)),
        maxX: d3.max(src, line => d3.max(line, o => o.x)),
        maxY: d3.max(src, line => d3.max(line, o => o.y))
      }
    }
  },
  @computed('scale', 'interpolate') dfunc(scale, ip) {
    return d3.svg.line().interpolate(ip).x((d, i) => scale.x(i)).y(d => scale.y(d));
  },
  @computed('src.[]') color(src) {
    return d3.scale.category10();
  },
  @computed('src.[]', 'dfunc', 'color') ds(src, dfunc, color) {
    return src.map(function(e, i) {
      return {
        line: dfunc(e),
        color: color(i)
      };
    });
  },
  @computed() zoom() {
    console.log('compute zoom');
    const self = this;
    return d3.behavior
      .zoom()
      .scaleExtent([0.6, 2])
      .on('zoom', function() { self.invalidate(); });
  },
  @computed('vb.width', 'vb.height', 'mmXY', 'zoom') scale(w, h, mmXY, zoom) {
    const {minX, minY, maxX, maxY} = mmXY;
    const scale = {
      x: d3.scale.linear().domain([minX, maxX]).range([0, w]),
      y: d3.scale.linear().domain([minY, maxY]).range([h, 0])
    };
    const prevScale = zoom.scale();
    const prevTrans = zoom.translate();
    zoom.x(scale.x).y(scale.y).scale(prevScale).translate(prevTrans);
    d3.select(this.element).on('.zoom', null).call(zoom);
    return scale;
  },
  @computed('scale.x', 'attrs.curIndex') vIndex(sx, index) {
    return sx(index.value) || 0;
  },
  invalidate() {
    ['gAxis', 'ds'].forEach(this.notifyPropertyChange, this);
  },
  @computed('vb.width', 'vb.height', 'scale') axis(w, h, scale) {
    const axisX = d3.svg.axis().tickPadding(10).tickSubdivide(true);
    const axisY = d3.svg.axis().tickPadding(10).tickSubdivide(true);
    return {
      x: axisX.scale(scale.x).tickSize(-h).orient('bottom'),
      y: axisY.scale(scale.y).tickSize(-w).orient('left')
    }
  },
  @computed('vb.width', 'vb.height', 'axis') gAxis(w, h, axis) {
    const gX = document.createElement('g');
    const gY = document.createElement('g');
    gX.className = 'x axis';
    gX.setAttribute('transform', `translate(0, ${h})`);
    gY.className = 'y axis';
    axis.x(d3.select(gX));
    axis.y(d3.select(gY));
    return {y: gY, x: gX};
  }
});
