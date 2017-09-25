import Ember from 'ember';
import computed, { observes } from 'ember-computed-decorators';

/* global Chart */

const yAxes = {
  type: 'linear',
  position: 'left',
  gridLines: {
    color: 'rgba(255, 255, 255, 0.5)',
    display: false
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
    labelString: 'Orientation of Stimulus'
  },
  gridLines: {
    display: false,
    color: 'rgba(255, 255, 255, 0.5)',
    // drawOnChartArea: false,
    // drawTicks: true
  },
  ticks: {
    maxTicksLimit: 32
  }
}

const type = 'lineEx';
const data = { labels:[], datasets:[] }; // dummy
const options = {
  title: {
    // display: true,
    // text: 'Response Overview',
    // fontStyle: 'normal'
  },
  legend: {display: false},
  tooltips: {enabled: true},
  scales: {
    yAxes: [yAxes],
    xAxes: [xAxes],
  },
  hover: {
    animationDuration: null
  },
  elements: {
    // line: {
    //   borderWidth: 1,
    //   fill: false,
    //   tension: 0
    // },
    point: {
      radius: 0,
      hoverRadius: 8,
      hitRadius: 8
    }
  },
  animation: {
    duration: null
  }
};
const Data = Ember.Object.extend({
  array: [],
  @computed('array') labels(array) {
    return array.map((e, i) => i);
  },
  @computed('array') datasets(array) {
    return [{
      borderColor: 'rgba(255, 0, 0, 1)',
      borderWidth: 0.5,
      data: array,
    }];
  }
});
export default Ember.Component.extend({
  tagName: 'canvas',
  width: 256,
  height: 54,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed() config() { return { type, data, options }; },
  @computed('src') data(src={}) { return Data.create(src); },
  labels: Ember.computed.alias('data.labels'),
  datasets: Ember.computed.alias('data.datasets'),
  @computed('ctx', 'config') chart(ctx, cfg) { return new Chart(ctx, cfg); },
  draw: function() {
    const {chart, labels, datasets
    } = this.getProperties('chart', 'labels', 'datasets');
    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
  }.observes('src'),
  @observes('index') drawIndex() {
    const index = parseInt(this.get('index'));
    this.get('chart').anon.controller.setIndex(index);
  },
  initialize: function() {
  }.on('didInsertElement'),
  dnitialize: function() {
    this.get('chart').destroy();
  }.on('willDestroyElement')
});
