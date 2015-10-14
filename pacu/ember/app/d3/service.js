import Ember from 'ember';
import computed from 'ember-computed-decorators';
import d3 from 'd3';

const defaultMargin = {
  top   : 20,
  right : 30,
  bottom: 30,
  left  : 30
}

const D3Convention = Ember.Object.extend({
  @computed('vpWidth', 'margin.left', 'margin.right') width(w, l, r) {
    return w - l - r;
  },
  @computed('vpHeight', 'margin.top', 'margin.bottom') height(h, t, b) {
    return h - t - b;
  },
  @computed('vpWidth', 'vpHeight', 'margin.left', 'margin.top') svg(vpw, vph, ml, mt) {
    return d3.select('body').append('svg').attr({
      width: vpw, height: vph, viewBox: `${-ml} ${-mt} ${vpw} ${vph}`
    });
  },
  scale(minX, minY, maxX, maxY) {
    const {width, height} = this.getProperties('width', 'height');
    return {
      x: d3.scale.linear().domain([minX, maxX]).range([0, width]),
      y: d3.scale.linear().domain([minY, maxY]).range([height, 0])
    };
  },
  axis(x, y) {
    const {width, height} = this.getProperties('width', 'height');
    const axisX = d3.svg.axis().tickPadding(10).tickSubdivide(true);
    const axisY = d3.svg.axis().tickPadding(10).tickSubdivide(true);
    return {
      xAxis: axisX.scale(x).tickSize(-height).orient("bottom"),
      yAxis: axisY.scale(y).tickSize(-width).orient("left")
    }
  },
  zoom(x, y, zfunc) {
    return d3.behavior.zoom().x(x).y(y).scaleExtent([0.8, 2]).on('zoom', zfunc);
  }
});

export default Ember.Service.extend({
  convention(vpWidth, vpHeight, margin=defaultMargin) {
    return D3Convention.create({vpWidth, vpHeight, margin: Ember.Object.create(margin)});
  }
});
