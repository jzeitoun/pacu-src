import Ember from 'ember';
import computed from 'ember-computed-decorators';

const yAxes = {
  type: 'linear',
  position: 'left',
  gridLines: {
    color: 'rgba(255, 255, 255, 0.25)',
    zeroLineColor: 'rgba(255, 255, 255, 0.5)',
    drawTicks: false,
    display: true
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
    drawOnChartArea: true,
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
    text: 'SF Tuning Curve',
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
      radius: 3,
      backgroundColor: 'rgba(5,5,5,1)',
      borderColor: 'rgba(255,255,255,1)',
      hoverRadius: 0,
      hitRadius: 0
    }
  }
};

const Data = Ember.Object.extend({
   indices: {},
   sfx: [],
   sfy: [],
   dog_x: [],
   dog_y: [],
   @computed('sfx') labels(x) {
     return x.map((e, i) => e);
   },
   @computed('sfy') datasets(y) {
     return [
       // {
       //   borderColor: 'rgba(0, 255, 255, 1)',
       //   borderWidth: 0.5,
       //   data: y,
       // },
       {
         borderColor: 'rgba(255, 255, 255, 0.5)',
         borderWidth: 1,
         data: y,
       },
     ];
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
  indices: Ember.computed.alias('data.indices'),
  labels: Ember.computed.alias('data.labels'),
  datasets: Ember.computed.alias('data.datasets'),
  @computed('ctx', 'config') chart(ctx, cfg) { return new Chart(ctx, cfg); },
  draw: function() {
    const {chart, labels, datasets, indices
    } = this.getProperties('chart', 'labels', 'datasets', 'indices');
    // const ticks = chart.config.options.scales.xAxes[0].ticks;
    // ticks.userCallback = (value, index, values) => indices[index];
    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
  }.observes('src').on('didInsertElement'),
  dinitialize: function() {
    this.get('chart').destroy();
  }.on('willDestroyElement')
});
