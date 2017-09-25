import Ember from 'ember';
import computed from 'ember-computed-decorators';

/* global Chart */

const yFAxes = {
  type: 'linear',
  position: 'left',
  gridLines: {
    display: true,
    color: 'rgba(255, 255, 255, 0.5)',
    zeroLineColor: 'rgba(255, 255, 255, 0.5)',
    drawOnChartArea: false,
    drawTicks: false,
  },
  scaleLabel: {
    display: false,
  },
  ticks: {
    display: true,
    beginAtZero: true,
    min: 0,
    max: 1
  }
};
const xFAxes = {
  type: 'category',
  position: 'bottom',
  scaleLabel: {
    display: false,
  },
  gridLines: {
    display: true,
    color: 'rgba(255, 255, 255, 0.5)',
    zeroLineColor: 'rgba(255, 255, 255, 0.5)',
    drawOnChartArea: false,
    drawTicks: false
  },
  ticks: {
    display: false,
    autoSkip: false,
  },
};
const yMAxes = {
  type: 'linear',
  position: 'left',
  gridLines: {
    display: true,
    color: 'rgba(255, 255, 255, 0.5)',
    zeroLineColor: 'rgba(255, 255, 255, 0.5)',
    drawOnChartArea: false,
    drawTicks: false,
  },
  scaleLabel: {
    display: false,
  },
  ticks: {
    display: true,
    beginAtZero: true,
    min: 0,
    max: 1
  }
};
const xMAxes = {
  type: 'category',
  position: 'bottom',
  scaleLabel: {
    display: false,
  },
  gridLines: {
    display: true,
    color: 'rgba(255, 255, 255, 0.5)',
    zeroLineColor: 'rgba(255, 255, 255, 0.5)',
    drawOnChartArea: false,
    drawTicks: false
  },
  ticks: {
    display: false,
    autoSkip: false,
    userCallback: function(value, index /*, values*/) {
      return index == 0 ? 'F': value;
    }
  },
};



const FType = 'line';
const FData = { labels:[], datasets:[] }; // dummy
const FOptions =  {
  title: {
    display: true,
    text: 'SF Tuning Curve',
    fontStyle: 'normal'
  },
  legend: {display: false},
  tooltips: {enabled: false},
  scales: {
    yAxes: [yFAxes],
    xAxes: [xFAxes],
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


const MType = 'line';
const MData = { labels:[], datasets:[] }; // dummy
const MOptions =  {
  title: {
    display: true,
    text: 'SF Tuning Curve',
    fontStyle: 'normal'
  },
  legend: {display: false},
  tooltips: {enabled: true},
  scales: {
    yAxes: [yMAxes],
    xAxes: [xMAxes],
  },
  elements: {
    line: {
      borderWidth: 1,
      fill: false,
      tension: 0
    },
    point: {
      radius: 4,
      hoverRadius: 2,
      hitRadius: 0
    }
  }
};

const Data = Ember.Object.extend({
   // indices: {},
   sfx: [],
   sfy: [],
   dog_x: [],
   dog_y: [],
   @computed('dog_x') FLabels(x) {
     return x.map(e => e);
   },
   @computed('sfx') MLabels(x) {
     return x.map(e => e);
   },
   @computed('dog_y') FDatasets(y) {
     return [
       {
         borderColor: 'rgba(255, 0, 0, 1)',
         borderWidth: 1,
         data: y,
       },
     ];
   },
   @computed('sfy') MDatasets(y) {
     return [
       {
         borderColor: 'rgba(255, 255, 255, 1)',
         borderWidth: 1,
         data: y,
       },
     ];
   }
});


export default Ember.Component.extend({
  @computed() FCtx() { return this.$('#sfreq-fitting').get(0).getContext('2d'); },
  @computed() MCtx() { return this.$('#sfreq-measure').get(0).getContext('2d'); },
  @computed() FConfig() { return {
    type: FType,
    data: FData,
    options: FOptions
    };
  },
  @computed() MConfig() { return {
    type: MType,
    data: MData,
    options: MOptions
    };
  },
  @computed('FCtx', 'FConfig') FChart(ctx, cfg) { return new Chart(ctx, cfg); },
  @computed('MCtx', 'MConfig') MChart(ctx, cfg) { return new Chart(ctx, cfg); },
  @computed('src') Data(src={}) { return Data.create(src); },
  FLabels: Ember.computed.alias('Data.FLabels'),
  MLabels: Ember.computed.alias('Data.MLabels'),
  FDatasets: Ember.computed.alias('Data.FDatasets'),
  MDatasets: Ember.computed.alias('Data.MDatasets'),
  initialize: function() {

    const {FChart, FLabels, FDatasets
    } = this.getProperties('FChart', 'FLabels', 'FDatasets');
    const {MChart, MLabels, MDatasets
    } = this.getProperties('MChart', 'MLabels', 'MDatasets');

    const mMin = Math.min(...MDatasets[0].data);
    const mMax = Math.max(...MDatasets[0].data);
    const fMin = Math.min(...FDatasets[0].data);
    const fMax = Math.max(...FDatasets[0].data);
    const min = Math.min(mMin, fMin);
    const max = Math.max(mMax, fMax);

    MChart.config.options.scales.yAxes[0].ticks.min = min;
    MChart.config.options.scales.yAxes[0].ticks.max = max;
    FChart.config.options.scales.yAxes[0].ticks.min = min;
    FChart.config.options.scales.yAxes[0].ticks.max = max;

    FChart.data.labels = FLabels;
    FChart.data.datasets = FDatasets;
    MChart.data.labels = MLabels;
    MChart.data.datasets = MDatasets;
    FChart.update();
    MChart.update();

  }.observes('src').on('didInsertElement'),
   dinitialize: function() {
     this.get('FChart').destroy();
     this.get('MChart').destroy();
   }.on('willDestroyElement')
});




//    tagName: 'canvas',
//    width: 100,
//    height: 100,
//    attributeBindings: ['width', 'height'],
//    indices: Ember.computed.alias('data.indices'),
    // const ticks = chart.config.options.scales.xAxes[0].ticks;
    // ticks.userCallback = (value, index, values) => indices[index];









// var doughnutData1 = {
//   labels: ["R", "G", "B"],
//   datasets: [{
//     data: [300, 50, 100],
//     backgroundColor: ["red", "green", "blue"],
//   }]
// };
// var doughnutData2 = {
//   labels: ["C", "Y", "M"],
//   datasets: [{
//     data: [30, 10, 80],
//     backgroundColor: ["cyan", "yellow", "magenta"],
//   }]
// };
// export default Ember.Component.extend({
//   initialize: function() {
//     var ctx1 = $("#sfreq-fitting").get(0).getContext("2d");
//     var myChart1 = new Chart(ctx1, {
//       type: 'doughnut',
//       data: doughnutData1,
//     });
//     var ctx2 = $("#sfreq-measure").get(0).getContext("2d");
//     var myChart2 = new Chart(ctx2, {
//       type: 'doughnut',
//       data: doughnutData2,
//     });
//   }.on('didInsertElement')
// });
