import Ember from 'ember';
import computed, { on, observes } from 'ember-computed-decorators';

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
const data = { labels:[], datasets:[] }; // dummy as an initial data
const options =  {
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
      tension: 0
    },
    point: {
      radius: 0,
      hoverRadius: 0,
      hitRadius: 0
    }
  },
  animation: { // important
    duration: null,
  }
};
const config = { type, data, options }

const DataFetcher = Ember.Object.extend({
  @computed('datatag') orientations(datatag) {
    // if (Ember.isNone(datatag)) { return []; }
    return datatag.get('value.orientations') || [];
  },
  @computed('datatag') datasets(datatag) {
    // if (Ember.isNone(datatag)) { return []; }
    const y_meas = datatag.get('value.y_meas') || [];
    const y_fit = datatag.get('value.y_fit') || [];
    const measureData = {
      borderColor: 'rgba(255, 255, 255, 1)',
      borderWidth: 0.5,
      data: y_meas,
    };
    const fitData = {
      borderColor: 'rgba(255, 0, 0, 1)',
      borderWidth: 1,
      data: y_fit,
    };
    return [measureData, fitData];
  },
  @computed('datatag') labels(datatag) {
    // if (Ember.isNone(datatag)) { return []; }
    return datatag.get('value.x') || [];
  },
});

export default Ember.Component.extend({
  tagName: 'canvas',
  classNames: 'noselect',
  width: 500,
  height: 96,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed('ctx') chart(ctx) { return new Chart(ctx, config); },
  // @observes('datapromise') promiseIncoming() {
  //   const prom = this.get('datapromise');
  //   if (Ember.isNone(prom)) {
  //     this.set('datatag', {});
  //   } else {
  //     prom.then(data => {
  //       this.set('datatag', data.get('firstObject.value'));
  //     });
  //   }
  // },
  datatag: Ember.Object.create({ value: {} }),
  @computed('datatag') fetcher(datatag) {
    return DataFetcher.create({ datatag });
  },
  // @observes('dimension.width') dimensionChanged() {
  //   this.get('chart').update();
  // },
  @observes('datatag') draw() {
    const {chart, fetcher, roiID} = this.getProperties('chart', 'fetcher', 'roiID');
    // if (Ember.$.isEmptyObject(this.get('datatag'))) {
    //   chart.data.datasets = datasets;
    //   chart.update();
    //   return;
    // }
    const labels = fetcher.get('labels');
    const datasets = fetcher.get('datasets');
    const orientations = fetcher.get('orientations');
    const ticks = chart.config.options.scales.xAxes[0].ticks;
    ticks.callback = (value, index, values) => {
      if (orientations.includes(value)) {
        return value;
      }
    };
    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
  },
  @on('didInsertElement') initialize() {
    Ember.run.next(this, 'draw');
  },
  @on('willDestroyElement') dnit() {
    this.get('chart').destroy();
  }
});
