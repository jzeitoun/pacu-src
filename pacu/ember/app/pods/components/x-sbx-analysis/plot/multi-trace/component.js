import Ember from 'ember';
import computed, { on, observes } from 'ember-computed-decorators';
import Manager from 'pacu/pods/components/x-sbx-analysis/plot/multi-trace/chart';

export default Ember.Component.extend({
  tagName: 'canvas',
  width: 500,
  height: 128,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed('ctx') chart(ctx) { return new Chart(ctx, Manager.config); },
  @observes('traces.@each.array') draw() {
    const traces = this.get('traces');
    const manager = Manager.create({traces: traces.map(t => t.toJSON())});
    const chart = this.get('chart');
    chart.data.labels = manager.get('labels');
    chart.data.datasets = manager.get('datasets');
    chart.update();
  },
  @on('didInsertElement') initialize() { },
  @on('willDestroyElement') dnitialize() {
    this.get('chart').destroy();
  }
});
