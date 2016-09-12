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
  },
  animation: { // important
    duration: null,
  }
};
const config = { type, data, options }

const DataFetcher = Ember.Object.extend({
  // mean: [],
  @computed('datatags.@each.value') unavailable(datatags=[[]]) {
    return datatags.getEach('value').any(Ember.isNone);
  },
  @computed('datatags.@each.value') byTrials(datatags=[[]]) {
    const byTrials = [];
    const dts = datatags.copy();
    // making 2d array
    const nReps = this.get('condition.repetition');
    while (dts.length) { byTrials.push(dts.splice(0, nReps)); }
    return byTrials;
  },
  @computed('byTrials') meantrace(byTrials) {
    const mt = byTrials.map(t => {
      var ons = t.map(r=>r.get('value.on'));
      var onsT = ons[0].map((_, i) => ons.map(row => row[i]));
      var onmean = onsT.map( dp => dp.reduce((a, b) => a + b) / dp.length);
      var bss = t.map(r=>r.get('value.baseline'));
      var bssT = bss[0].map((_, i) => bss.map(row => row[i]));
      var bsmean = bssT.map( dp => dp.reduce((a, b) => a + b) / dp.length);
      return { on: onmean, baseline: bsmean }
    })
    return mt;
  },
  @computed('byTrials') byReps(byTrials) {
    // transpose it
    return byTrials[0].map((_, i) => byTrials.map(row => row[i]));
  },
  @computed('meantrace', 'byReps') datasets(meantrace, byReps) {
    const borderColor = 'rgba(255, 255, 255, 0.5)';
    const borderWidth = 0.5;
    const datasets = byReps.map(rep => {
      let data = [].concat(...rep.map(trial => {
        if (Ember.isEmpty(trial)) { return []; }
        let {baseline, on} = trial.get('value');
        return [].concat(baseline, on);
      }));
      return { data, borderColor, borderWidth };
    });
    datasets.push({
      data: [].concat(...meantrace.map(mt => [].concat(mt.baseline, mt.on))),
      borderColor: "rgba(255, 0, 0, 1)", borderWidth: 1.5
    });
    return datasets;
  },
  @computed('datasets') labels(datasets) {
    return datasets[0].data.map((e, i) => i);
  },
  @computed('byReps') indices(byReps) {
    const reps = byReps[0];
    const indices = {};
    let index = 0;
    try {
      for (let rep of reps) {
        if (Ember.isEmpty(rep)) { continue; }
        const on = rep.get('value.on');
        const baseline = rep.get('value.baseline');
        const ori = rep.get('trial_ori');
        index += baseline.length;
        indices[index] = ori;
        index += on.length;
      }
      return indices;
    } catch(err) {
      console.log('Unable to generate indices', err);
      return [];
    }
  }
});

export default Ember.Component.extend({
  tagName: 'canvas',
  classNames: 'noselect',
  width: 500,
  height: 96,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed('ctx') chart(ctx) {
    const self = this;
    const chart = new Chart(ctx, config);
    const draw = chart.draw;
    chart.draw = function() {
      draw.apply(this, arguments);
      self.chartDidDraw(this, ...arguments);
    };
    return chart;
  },

  @observes('datapromise') promiseIncoming() {
    const prom = this.get('datapromise');
    if (Ember.isNone(prom)) {
      this.set('datatags', [[]]);
    } else {
      prom.then(dts => {
        this.set('datatags', dts.sortBy('trial_ori'));
      });
    }
  },
  @computed('condition', 'datatags.@each.updated_at') fetcher(condition, datatags) {
    return DataFetcher.create({ datatags, condition });
  },
  @observes('dimension.width') dimensionChanged() {
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
    try {
      chart.boxes[2].options.text = `Orientation of Stimulus - #${roiID}`
      const {datasets, labels, indices} = fetcher.getProperties(
        'datasets', 'labels', 'indices');
      const ticks = chart.config.options.scales.xAxes[0].ticks;
      ticks.userCallback = (value, index, values) => indices[index];
      chart.data.labels = labels;
      chart.data.datasets = datasets;
      chart.update();
    } catch (err) {
      console.log('Orientations of Stimulus faild to plot', err);
    }
  },
  chartDidDraw(chart) {
    const fetcher = this.get('fetcher');
    const indices = fetcher.get('indices');
    let len = fetcher.get('byReps')[0][0].get('value.on.length');
    let { top, height } = chart.scales['y-axis-0'];
    let width = chart.scales['x-axis-0'].getPixelForTick(len) - chart.scales['x-axis-0'].getPixelForTick(0);
    chart.chart.ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
    for (let x in indices) {
      let x0 = chart.scales['x-axis-0'].getPixelForTick(parseInt(x));
      chart.chart.ctx.fillRect(x0, top, width, height);
    }
  },
  @on('willDestroyElement') dnit() {
    console.log('destroy orientations charts...');
    this.get('chart').destroy();
  }
});
