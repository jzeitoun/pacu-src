import Ember from 'ember';
import computed, { on, observes } from 'ember-computed-decorators';
import Manager from 'pacu/pods/components/x-sbx-analysis/plot/ephys-correlation-traces/chart';

export default Ember.Component.extend({
  tagName: 'canvas',
  classNames: 'noselect',
  width: 120,
  height: 64,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed('ctx') chart(ctx) { return new Chart(ctx, Manager.config); },
  @observes('traces') draw() {
    const traces = this.get('traces');
    const manager = Manager.create({traces});
    const chart = this.get('chart');
    chart.data.labels = manager.get('labels');
    chart.data.datasets = manager.get('datasets');
    chart.update();
  },
});
