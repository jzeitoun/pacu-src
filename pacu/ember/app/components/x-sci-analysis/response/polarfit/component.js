import Ember from 'ember';
import computed from 'ember-computed-decorators';

const rAxes = {
  type: 'radialLinear',
  lineArc: true,
  gridLines: {
    display: true,
    color: 'rgba(100, 100, 100, 0.1)',
  },
  pointLabels: {
    fontSize: 6
  },
  ticks: {
    display: false,
    beginAtZero: true
  }
}
const type = 'radar';
const data = { labels: [], datasets: [] }; // dummy
const options = {
  title: {
    display: false,
  },
  legend: {display: false},
  tooltips: {enabled: false},
  scale: rAxes,
  elements: {
    line: {
      borderWidth: 1,
      fill: false,
      tension: 0
    },
    point: {
      radius: 0,
      hoverRadius: 0,
      hitRadius: 0
    }
  }
};
const Data = Ember.Object.extend({
  names: [],
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
  width: 100,
  height: 100,
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
    // const ticks = chart.config.options.scale.ticks;
    // ticks.callback = (value, index, values) => {
    //   console.log(value, index);
    //   if (names.indexOf(value) > -1) {
    //     return value;
    //   }
    // };
    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
  }.observes('src'),
  dinitialize: function() {
    this.get('chart').destroy();
  }.on('willDestroyElement')
});
