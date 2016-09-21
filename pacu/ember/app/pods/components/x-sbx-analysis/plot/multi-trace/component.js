import Ember from 'ember';
import computed, { on, observes } from 'ember-computed-decorators';
import Manager from 'pacu/pods/components/x-sbx-analysis/plot/multi-trace/chart';

export default Ember.Component.extend({
  tagName: 'canvas',
  classNames: 'noselect',
  classNameBindings: ['augKeyOn'],
  width: 500,
  height: 128,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed('ctx') chart(ctx) { return new Chart(ctx, Manager.config); },
  @observes('datatags') draw() {
    const datatags = this.get('datatags');
    const chart = this.get('chart');
    const manager = Manager.create({ datatags });
    chart.data.labels = manager.get('labels');
    chart.data.datasets = manager.get('datasets');
    chart.update();
    this.set('dimension.width', chart.scales['y-axis-0'].width);
  },
  @observes('index') drawIndex() {
    const index = parseInt(this.get('index'));
    const chart = this.get('chart');
    if (chart.anon) {
      chart.anon.controller.setIndex(index);
    }
  },
  @on('didInsertElement') initialize() {
    // Ember.$(document).on('keydown.multi-trace', ({altKey, metaKey}) => {
    //   this.set('augKeyOn', altKey || metaKey);
    // });
    // Ember.$(document).on('keyup.multi-trace', () => {
    //   this.set('augKeyOn', false);
    // });
    // this.get('datatags').then(dts => {
    // });
    // console.log('CHART DID INSERT ELEMENT', 'PREP EMPTY DIMENSION');
    Ember.run.next(this, 'draw');
    // const chart = this.get('chart');
    // chart.update();
    // this.set('dimension.width', chart.scales['y-axis-0'].width);
  },
  // @on('didUpdateAttrs') didupdateattrs() {
  //   console.log('CHART didUpdateAttrs', ...arguments);
  // },
  // @on('didReceiveAttrs') didrecieveattrs() {
  //   console.log('CHART didRecieveAttrs', ...arguments);
  // },
  // @on('willRender') willrender() {
  //   console.log('CHART WILL RENDER', ...arguments);
  // },
  // @on('didRender') didrender() {
  //   console.log('CHART DID RENDER', ...arguments);
  // },
  @on('willDestroyElement') dnitialize() {
    this.get('chart').destroy();
    // Ember.$(document).off('keydown.multi-trace');
    // Ember.$(document).off('keyup.multi-trace');
  },
  // mouseMove(e) {
  //   const on = this.get('augKeyOn');
  // }
});
