import Ember from 'ember';
import computed from 'ember-computed-decorators';

/* global Chart */

const yAxes = {
  type: 'linear',
  position: 'left',
  gridLines: {
    color: 'rgba(255, 255, 255, 0.5)',
    display: false
  },
  scaleLabel: {
    display: true,
    labelString: 'dF/F0'
  },
  ticks: { display: true, }
};
const xAxes = {
  type: 'category',
  position: 'bottom',
  scaleLabel: {
    display: false,
    labelString: 'Orientation of Stimulus'
  },
  gridLines: {
    display: false,
    color: 'rgba(255, 255, 255, 0.5)',
    // drawOnChartArea: false,
    // drawTicks: true
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
    text: 'Orientation of Stimulus',
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
  @computed('mean') labels(mean) {
    return mean.map((e, i) => i);
  },
  @computed('traces', 'mean') datasets(traces, mean) {
    const ds = [{
      borderColor: 'rgba(0, 255, 255, 1)',
      borderWidth: 0.5,
      data: mean,
    }];
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
  width: 220,
  height: 80,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed() config() { return { type, data, options }; },
  @computed('src') data(src={}) { return Data.create(src); },
  indices: Ember.computed.alias('data.indices'),
  labels: Ember.computed.alias('data.labels'),
  datasets: Ember.computed.alias('data.datasets'),
  @computed('ctx', 'config') chart(ctx, cfg) { return new Chart(ctx, cfg); },
  draw: function() {
    const {chart, labels, datasets, indices
    } = this.getProperties('chart', 'labels', 'datasets', 'indices');
    const ticks = chart.config.options.scales.xAxes[0].ticks;
    ticks.userCallback = (value, index /*, values*/) => indices[index];
    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
  }.observes('src'),
  dinitialize: function() {
    this.get('chart').destroy();
  }.on('willDestroyElement')
});
