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
    // labelString: 'Orientation of Stimulus'
  },
  gridLines: {
    display: false,
    color: 'rgba(255, 255, 255, 0.5)',
    // drawOnChartArea: false,
    // drawTicks: true
  },
  ticks: {
    maxTicksLimit: 24
  }
}

const type = 'lineEx';
const data = { labels:[], datasets:[] }; // dummy
const options = {
  title: {
    display: true,
    text: 'ROI Traces',
    fontStyle: 'normal'
  },
  legend: {
    display: true,
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
      hoverRadius: 8,
      hitRadius: 8,
    }
  },
  animation: {
    duration: null
  }
};

export default Ember.Object.extend({
  @computed('traces') labels(traces) {
    const lens = traces.map(t => t.array.length);
    if (Ember.isEmpty(lens)) { return []; }
    return Array.from(Array(Math.max(...lens)).keys()); // range the JS way.
  },
  @computed('traces') datasets(traces) {
    return traces.map((trace, index) => {
      return {
        borderColor: trace.color || color.google20[index],
        borderWidth: 0.5,
        data: trace.array,
        label: `ROI #${trace.roi}`,
      }
    });
  }
}).reopenClass({config: { type, data, options }});
