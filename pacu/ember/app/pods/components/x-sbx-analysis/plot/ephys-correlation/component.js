import Ember from 'ember';
import computed, { on, observes } from 'ember-computed-decorators';
import Manager from 'pacu/pods/components/x-sbx-analysis/plot/ephys-correlation/chart';

export default Ember.Component.extend({
  tagName: 'canvas',
  classNames: 'noselect',
  width: 120,
  height: 40,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed('ctx') chart(ctx) { return new Chart(ctx, Manager.config); },
  @observes('meantrace') draw() {
    const meantrace = this.get('meantrace');
    const manager = Manager.create({meantrace});
    const chart = this.get('chart');
    chart.data.labels = manager.get('labels');
    chart.data.datasets = manager.get('datasets');
    chart.update();
  },
});
