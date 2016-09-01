import Ember from 'ember';
import computed, { on, observes } from 'ember-computed-decorators';

const yAxes = {
  type: 'linear',
  position: 'left',
  gridLines: {
    color: 'rgba(255, 255, 255, 0.5)',
    display: false
  },
  scaleLabel: {
    display: true,
    labelString: 'dF/F0',
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
const data = { labels:[], datasets:[] }; // dummy as an initial data
const options =  {
  title: {
    display: true,
    text: 'Orientation of Stimulus?',
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
const config = { type, data, options }

const DataFetcher = Ember.Object.extend({
  // mean: [],

  @computed('datatags.@each.value') unavailable(datatags=[[]]) {
    return datatags.getEach('value').any(Ember.isNone);
  },
  @computed('datatags.@each.value') byReps(datatags=[[]]) {
    const byTrials = [];
    const dts = datatags.copy();
    // making 2d array
    while (dts.length) { byTrials.push(dts.splice(0, 2)); }
    // transpose it
    return byTrials[0].map((_, i) => byTrials.map(row => row[i]));
  },
  @computed('byReps') datasets(byReps) {
    const borderColor = 'rgba(255, 255, 255, 0.1)';
    return byReps.map(rep => {
      let data = [].concat(...rep.map(trial => {
        if (Ember.isEmpty(trial)) { return []; }
        let {baseline, on} = trial.get('value');
        return [].concat(baseline, on);
      }));
      return { data, borderColor };
    })
  },
  @computed('datasets') labels(datasets) {
    return datasets[0].data.map((e, i) => i);
  },
  @computed('byReps') indices(byReps) {
    const reps = byReps[0];
    const indices = {};
    let index = 0;
    for (let rep of reps) {
      if (Ember.isEmpty(rep)) { continue; }
      const on = rep.get('value.on');
      const baseline = rep.get('value.baseline');
      const ori = rep.get('trial.ori');
      index += baseline.length;
      indices[index] = ori;
      index += on.length;
    }
    return indices;
  }
});

export default Ember.Component.extend({
  tagName: 'canvas',
  classNames: 'noselect',
  width: 500,
  height: 96,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed('ctx') chart(ctx) { return new Chart(ctx, config); },
  @computed('datatags') fetcher(datatags) {
    console.log('generating controller');
    return DataFetcher.create({ datatags });
  },
  @observes('dimension.width') dimensionChanged() {
    console.log('dimenstion chanenge for orientations');
    this.get('chart').update();
  },
  @observes('datatags') draw() {
    const {chart, fetcher, roiID} = this.getProperties('chart', 'fetcher', 'roiID');
    if (Ember.isNone(roiID)) {
      chart.boxes[2].options.text = 'Orientation of Stimulus - No selection'
      chart.data.datasets = [];
      chart.update();
      return;
    }
    if (fetcher.get('unavailable')) {
      chart.boxes[2].options.text = 'Orientation of Stimulus - No datatags'
      chart.data.datasets = [];
      chart.update();
      return;
    }
    window.C = chart;
    chart.boxes[2].options.text = `Orientation of Stimulus - #${roiID}`
    const {datasets, labels, indices} = fetcher.getProperties(
      'datasets', 'labels', 'indices');
    const ticks = chart.config.options.scales.xAxes[0].ticks;
    ticks.userCallback = (value, index, values) => indices[index];
    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
  },
  @on('willDestroyElement') dnit() {
    console.log('destroy orientations charts...');
    this.get('chart').destroy();
  }
});
