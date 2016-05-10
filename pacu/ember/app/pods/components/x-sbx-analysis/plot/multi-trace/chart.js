import Ember from 'ember';
import computed from 'ember-computed-decorators';
import color from 'pacu/utils/color';

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
}

const type = 'line';
const data = { labels:[], datasets:[] }; // dummy
const options = {
  title: {
    display: true,
    text: 'ROI Traces',
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

export default Ember.Object.extend({
  @computed('traces') labels(traces) {
    return Ember.isEmpty(traces) ? [] : traces[0].array.map((e,i) => i);
  },
  @computed('traces') datasets(traces) {
    return traces.map((trace, index) => {
      return {
        borderColor: trace.color || color.google20[index],
        borderWidth: 0.5,
        data: trace.array,
      }
    });
  }
}).reopenClass({config: { type, data, options }});
