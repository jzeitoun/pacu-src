import Ember from 'ember';
import computed, { on, observes } from 'ember-computed-decorators';
import Manager from 'pacu/pods/components/x-sbx-analysis/plot/ephys-trace/chart';

export default Ember.Component.extend({
  tagName: 'canvas',
  classNames: 'noselect',
  // classNameBindings: ['augKeyOn'],
  width: 500,
  height: 64,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed('ctx') chart(ctx) { return new Chart(ctx, Manager.config); },
  @observes('trace') draw() {
    const trace = this.get('trace');
    const manager = Manager.create({trace});
    const chart = this.get('chart');
    chart.data.labels = manager.get('labels');
    chart.data.datasets = manager.get('datasets');
    chart.update();
  },
  @observes('index') drawIndex() {
    const index = parseInt(this.get('index'));
    const chart = this.get('chart');
    if (chart.anon) {
      chart.anon.controller.setIndex(index);
    }
  },
  // @on('didInsertElement') initialize() {
  //   Ember.$(document).on('keydown.multi-trace', ({altKey, metaKey}) => {
  //     this.set('augKeyOn', altKey || metaKey);
  //   });
  //   Ember.$(document).on('keyup.multi-trace', () => {
  //     this.set('augKeyOn', false);
  //   });
  // },
  // @on('willDestroyElement') dnitialize() {
  //   this.get('chart').destroy();
  //   Ember.$(document).off('keydown.multi-trace');
  //   Ember.$(document).off('keyup.multi-trace');
  // },
  // mouseMove(e) {
  //   const on = this.get('augKeyOn');
  //   // if (on) {
  //   //   window.qwe = this.get('chart');
  //   //   window.asd = e;
  //   // }
  // }
});
