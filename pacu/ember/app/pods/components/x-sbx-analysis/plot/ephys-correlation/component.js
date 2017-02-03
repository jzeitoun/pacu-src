import Ember from 'ember';
import computed, { observes } from 'ember-computed-decorators';
import Manager from 'pacu/pods/components/x-sbx-analysis/plot/ephys-correlation/chart';

/* global Chart */

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
    const rmeantrace = this.get('rmeantrace');
    const manager = Manager.create({meantrace, rmeantrace});
    const chart = this.get('chart');
    chart.data.labels = manager.get('labels');
    chart.data.datasets = manager.get('datasets');
    chart.update();
  },
});
