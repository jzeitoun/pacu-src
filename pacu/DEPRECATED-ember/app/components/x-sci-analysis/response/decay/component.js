import Ember from 'ember';
import computed from 'ember-computed-decorators';

const yAxes = {
  type: 'linear',
  position: 'left',
  gridLines: {
    color: 'rgba(255, 255, 255, 0.5)',
    display: false
  },
  scaleLabel: {
    display: true,
    labelString: 'F'
  },
  ticks: { display: true, }
};
const xAxes = {
  type: 'category',
  position: 'bottom',
  scaleLabel: {
    display: false,
  },
  gridLines: {
    display: false,
    color: 'rgba(255, 255, 255, 0.5)',
    drawOnChartArea: false,
    drawTicks: true
  },
  ticks: {
    autoSkip: false,
    display: true,
    // userCallback: function(value, index, values) {
    //   return asd.repetition.indices[index];
    // }
  },
};

const type = 'line';
const data = { labels:[], datasets:[] }; // dummy
const options =  {
  title: {
    display: true,
    text: 'Decay at',
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
  traces: [[]],
  indices: {},
  mean: [],
  y_fit: [],
  name: '',
  @computed('name') text(name) {
    if (Ember.isEmpty(name)) { return 'Decay of max orientation'; }
    return `Decay at ${name}`;
  },
  @computed('mean') labels(mean) {
    return mean.map((e, i) => i);
  },
  @computed('traces', 'mean', 'y_fit') datasets(traces, mean, y_fit) {
    const ds = [
      {
        borderColor: 'rgba(0, 255, 255, 1)',
        borderWidth: 0.5,
        data: mean,
      },
      {
        borderColor: 'rgba(255, 0, 0, 1)',
        borderWidth: 1,
        data: y_fit,
      },
    ];
    for (let trace of traces) {
      ds.push({
        borderColor: 'rgba(255, 255, 255, 0.1)',
        data: trace,
      })
    }
    return ds;
  }
});

export default Ember.Component.extend({
  tagName: 'canvas',
  width: 100,
  height: 140,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed() config() { return { type, data, options }; },
  @computed('src') data(src={}) { return Data.create(src); },
  indices: Ember.computed.alias('data.indices'),
  labels: Ember.computed.alias('data.labels'),
  datasets: Ember.computed.alias('data.datasets'),
  text: Ember.computed.alias('data.text'),
  @computed('ctx', 'config') chart(ctx, cfg) { return new Chart(ctx, cfg); },
  draw: function() {
    const {chart, labels, datasets, indices, text
    } = this.getProperties('chart', 'labels', 'datasets', 'indices', 'text');
    const ticks = chart.config.options.scales.xAxes[0].ticks;
    chart.titleBlock.options.text = text;
    ticks.userCallback = (value, index, values) => indices[index];
    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
  }.observes('src').on('didInsertElement'),
  dinitialize: function() {
    this.get('chart').destroy();
  }.on('willDestroyElement')
});
