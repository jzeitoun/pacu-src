// import Ember from 'ember';

/* global Chart */

export function initialize(/* application */) {
  // application.inject('route', 'foo', 'service:foo');
  const LC = Chart.controllers.line;
  Chart.controllers.lineEx = LC.extend({
    initialize(/*chart, datasetIndex*/) {
      LC.prototype.initialize.apply(this, arguments);
      if (this.chart.anon) { return; }
      const main = this.chart.chart.canvas;
      this.chart.anon = document.createElement('canvas');
      this.chart.anon.classList.add('chart-js-anon', 'chart-js-anon-index');
      this.chart.anon.controller = this;
      main.style.position = 'absolute';
      main.classList.add('chart-js-main');
      main.parentNode.insertBefore(this.chart.anon, main.nextSibling);
    },
    update() {
      LC.prototype.update.apply(this, arguments);
      this.chart.anon.width = this.chart.chart.canvas.width;
      this.chart.anon.height = this.chart.chart.canvas.height;
      this.chart.anon.style.width = this.chart.chart.canvas.style.width;
      this.chart.anon.style.height = this.chart.chart.canvas.style.height;
      this.drawIndex();
    },
    setIndex(index) {
      this.chart.anon.index = index;
      this.drawIndex();
    },
    drawIndex() {
      const index = this.chart.anon.index;
      const dpr = this.chart.chart.currentDevicePixelRatio;
      const ctx = this.chart.anon.getContext('2d');
      const { top, bottom } = this.chart.scales['y-axis-0'];
      const xPix = this.chart.scales['x-axis-0'].getPixelForTick(index);
      ctx.clearRect(0, 0, this.chart.anon.width, this.chart.anon.height);
      ctx.beginPath();
      ctx.moveTo(xPix*dpr, top*dpr);
      ctx.lineTo(xPix*dpr, bottom*dpr);
      ctx.strokeStyle = '#ffffff';
      ctx.stroke();
    }
  });
}

export default {
  name: 'chartjs',
  initialize
};
