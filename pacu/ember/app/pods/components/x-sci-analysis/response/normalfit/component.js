import Ember from 'ember';
import computed from 'ember-computed-decorators';

const yAxes = {
  type: 'linear',
  position: 'left',
  gridLines: {
    color: 'rgba(255, 255, 255, 0.1)',
    zeroLineColor: 'rgba(255, 255, 255, 0.5)',
    display: true,
    drawTicks: false
  },
  scaleLabel: {
    display: false,
  },
  ticks: { display: true, }
}

const xAxes = {
  type: 'category',
  position: 'bottom',
  scaleLabel: {
    display: false,
    // labelString: 'Orientation of Stimulus'
  },
  gridLines: {
    display: true,
    color: 'rgba(255, 255, 255, 0.1)',
    zeroLineColor: 'rgba(255, 255, 255, 0.5)',
    drawTicks: false
  },
  ticks: {
    autoSkip: false,
    display: true,
  },
}

const type = 'line';
const data = { labels:[], datasets:[] }; // dummy
const options = {
  title: {
    display: true,
    text: 'Sum of Gaussians',
    fontStyle: 'normal'
  },
  legend: {display: false},
  tooltips: {enabled: false},
  scales: {
    yAxes: [yAxes],
    xAxes: [xAxes],
  },
  elements: {
    line: {
      borderWidth: 1,
      fill: false,
      tension: 1
    },
    point: {
      radius: 0,
      hoverRadius: 0,
      hitRadius: 0
    }
  }
};
const Data = Ember.Object.extend({
  stretched: [],
  fit: {x:[], y:[]},
  @computed('stretched', 'fit') labels(stretched, fit) {
    return fit.x.map((e, i) => i);
  },
  @computed('stretched', 'fit') datasets(stretched, fit) {
    const measureData = {
      borderColor: 'rgba(255, 255, 255, 1)',
      borderWidth: 0.5,
      data: stretched,
    };
    const fitData = {
      borderColor: 'rgba(255, 0, 0, 1)',
      borderWidth: 1,
      data: fit.y,
    };
    return [measureData, fitData];
  }
});
export default Ember.Component.extend({
  tagName: 'canvas',
  width: 220,
  height: 80,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed() config() { return { type, data, options }; },
  @computed('src') data(src={}) { return Data.create(src); },
  names: Ember.computed.alias('data.names'),
  labels: Ember.computed.alias('data.labels'),
  datasets: Ember.computed.alias('data.datasets'),
  @computed('ctx', 'config') chart(ctx, cfg) {
    return new Chart(ctx, cfg);
  },
  draw: function() {
    const {chart, labels, datasets, names
    } = this.getProperties('chart', 'labels', 'datasets', 'names');
    const ticks = chart.config.options.scales.xAxes[0].ticks;
    ticks.callback = (value, index, values) => {
      if (names.indexOf(value) > -1) {
        return value;
      }
    };
    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
  }.observes('src'),
  dinitialize: function() {
    this.get('chart').destroy();
  }.on('willDestroyElement')
});
