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
    labelString: 'dF/F0'
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
    autoSkip: false,
    display: true,
    userCallback: function(value, index, values) {
      return asd.repetition.indices[index];
    }
  },
}

export default Ember.Component.extend({
  tagName: 'canvas',
  width: 500,
  height: 200,
  attributeBindings: ['width', 'height'],
  @computed('ctx') chart(ctx) {
    return new Chart(ctx);
  },
  @computed() ctx() {
    return this.element.getContext('2d');
  },
  update: function() {
    // Chart.defaults.global.events = [];
    const src = this.get('src');
    if (Ember.isNone(src)) { return; }
    const ctx = this.get('ctx');
    const type = 'line';
    const data = this.get('data');
    const options = this.get('options');
    const chart = new Chart(ctx, {type, data, options});
  }.observes('src'),
  @computed('src') data(src) {
    console.log(src.repetition);
    const datasets = [{
          borderColor: 'rgba(256, 0, 0, 1)',
          data: src.repetition.mean,
    }];
    for (let trace of src.repetition.traces) {
      datasets.push({
        borderColor: 'rgba(256, 256, 256, 0.1)',
        data: trace,
      })
    }
    return {
      labels: src.repetition.mean.map((e, i) => i),
      datasets: datasets
    };
  },
  @computed() options() {
    return {
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
  },
});
