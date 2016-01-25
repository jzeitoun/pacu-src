import Ember from 'ember';
import computed from 'ember-computed-decorators';
import d3 from 'd3';

const data = [
  1.63308977, -0.87989681, -1.1828902 ,  1.0197694 , -0.06287617,
  0.48540695, -1.5992162 ,  1.16574355, -1.20482946, -0.52511011,
  0.60283645, -0.20084854, -0.01037821, -0.86664775,  1.73690916,
  0.97949734,  0.74491702,  1.27184386, -1.20041354,  0.41969183,
  1.22298902,  0.52658324,  0.16231463,  0.37506822,  0.21818095,
  0.93587734, -1.82813074, -0.20384137,  0.24365014,  0.15818588,
 -1.25465659,  0.52571763, -1.43325514,  1.90940593, -1.01042385,
  0.89668392, -1.5863214 ,  0.91936341,  1.41358154, -0.14348699,
 -0.3580974 ,  1.67867752,  1.14556951,  0.94555787, -0.85032138,
  0.10174647, -1.70645552,  1.23019235,  1.3462309 , -0.19088142,
 -0.78385738,  0.4979114 ,  0.29379298,  0.20023945, -1.15759602,
 -2.21300615,  0.35044871,  0.16943171,  0.71214213, -0.06734098,
  0.38048596, -0.56761883, -0.47896837, -0.89920645,  1.21204942,
  0.52452113, -1.06643311,  1.35290151,  0.18770474,  1.85155407,
 -0.87871745, -0.98880153, -0.33713155,  0.18704221,  1.54985222,
  0.78527487,  1.88416363,  1.34641582, -0.77547122,  0.90166426,
  0.12191185, -0.27120298,  0.22689822, -0.53233105, -0.35735504,
  0.15539328, -0.72944298,  0.34892427, -0.30718411, -0.14261494,
  0.25094014,  1.07713959,  0.22116695, -0.02458926,  1.53177259,
  0.79340718,  0.12135861,  0.40418279, -0.13923027,  0.51892575
]

export default Ember.Component.extend({
  tagName: 'canvas',
  width: 800,
  height: 300,
  attributeBindings: ['width', 'height'],
  @computed ctx() {
    return this.element.getContext('2d');
  },
  run: function() {
    const self = this;
    const src = '/Volumes/Gandhi Lab - HT/sbx/my4r_1_3_000_007'
    const qs = encodeURI(`?src=${src}`);
    console.log('refROI with', src);
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/api/ping/353/403/159/204${qs}`, true);
    xhr.responseType = 'arraybuffer';
    xhr.onload = function(e) {
      const arr = new Float32Array(this.response);
      console.log('DONE', arr);
      self.plot(arr);
    };
    xhr.onprogress = function(e) {
      console.log('on progress!', e);
      console.log('length computable?', e.lengthComputable);
      console.log(e.loaded, e.total);
    };
    xhr.send();
  }.on('didInsertElement'),
  plot: function(data) {
    const scaleY = d3.scale.linear().range([0, 300]).domain(d3.extent(data));
    const scaleX = d3.scale.linear().range([0, 800]).domain([0, data.length]);

    const ctx = this.get('ctx');
    ctx.beginPath();
    ctx.strokeStyle = '#0FF';
    ctx.lineWidth = 0.25;
    data.forEach(function(d, i) {
      ctx.lineTo(scaleX(i), scaleY(d));
    });
    ctx.stroke();
    ctx.closePath();

    // ctx.beginPath();
    // ctx.strokeStyle = '#FFF';
    // ctx.lineWidth = 0.5;
    // data.forEach(function(d, i) {
    //   ctx.moveTo(scaleX(i), 0);
    //   ctx.lineTo(scaleX(i), 800);
    // });
    // ctx.stroke();
    // ctx.closePath();

  }
});
