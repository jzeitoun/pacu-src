import Ember from 'ember';
import computed from 'ember-computed-decorators';
import Manager from 'pacu/components/x-sbx-analysis/plot/multi-trace/chart';

export default Ember.Component.extend({
  tagName: 'canvas',
  width: 500,
  height: 200,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed('over', 'by') manager(over, by) {
    return Manager.create({traces: over.filterBy('category', by)});
  },
  @computed('ctx') chart(ctx) { return new Chart(ctx, Manager.config); },
  draw: function() {
    const manager = this.get('manager');
    const chart = this.get('chart');
    chart.data.labels = manager.get('labels');
    chart.data.datasets = manager.get('datasets');
    chart.update();
  }.observes('over', 'by'),
  initialize: function() {
  }.on('didInsertElement'),
  dnitialize: function() {
    this.get('chart').destroy();
  }.on('willDestroyElement')
});
