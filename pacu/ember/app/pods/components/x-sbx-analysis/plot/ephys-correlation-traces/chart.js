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
    display: false,
    color: 'rgba(255, 255, 255, 0.5)',
    // drawOnChartArea: false,
    // drawTicks: true
  },
  ticks: {
    maxTicksLimit: 8
  }
}

const type = 'line';
const data = { labels:[], datasets:[] }; // dummy
const options = {
  title: {
    display: false,
    // text: 'ROI Traces',
    // fontStyle: 'normal'
  },
  legend: {
    display: false,
    labels: {
      fontSize: 10
    }
  },
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
      hoverRadius: 0,
      hitRadius: 0,
    }
  },
  animation: {
    duration: null
  }
};

export default Ember.Object.extend({
  @computed('traces') labels(traces=[[]]) {
    return traces[0].map((e, i) => i);
  },
  @computed('traces') datasets(traces=[[]]) {
    return traces.map(t => {
      return {
        borderColor: 'silver',
        borderWidth: 0.5,
        data: t,
      }
    });
  }
}).reopenClass({config: { type, data, options }});
