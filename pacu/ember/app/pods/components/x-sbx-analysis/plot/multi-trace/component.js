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
  @observes('datatags.@each.value') draw() {
    const datatags = this.get('datatags').map(t => t.toJSON());
    for (let dt of datatags) {
      if (Ember.isNone(dt.value)) dt.value = [];
    }
    const manager = Manager.create({traces: datatags});
    const chart = this.get('chart');
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
    Ember.$(document).on('keydown.multi-trace', ({altKey, metaKey}) => {
      this.set('augKeyOn', altKey || metaKey);
    });
    Ember.$(document).on('keyup.multi-trace', () => {
      this.set('augKeyOn', false);
    });
    this.draw();
  },
  @on('willDestroyElement') dnitialize() {
    this.get('chart').destroy();
    Ember.$(document).off('keydown.multi-trace');
    Ember.$(document).off('keyup.multi-trace');
  },
  mouseMove(e) {
    const on = this.get('augKeyOn');
    // if (on) {
    //   window.qwe = this.get('chart');
    //   window.asd = e;
    // }
  }
});
