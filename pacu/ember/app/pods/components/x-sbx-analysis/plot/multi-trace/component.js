import Ember from 'ember';
import computed from 'ember-computed-decorators';
import Manager from 'pacu/pods/components/x-sbx-analysis/plot/multi-trace/chart';

export default Ember.Component.extend({
  tagName: 'canvas',
  width: 500,
  height: 200,
  attributeBindings: ['width', 'height'],
  @computed() ctx() { return this.element.getContext('2d'); },
  @computed('traces') manager(traces) {
    console.log('getting tace', traces);
    return Manager.create({traces: traces});
  },
  @computed('ctx') chart(ctx) { return new Chart(ctx, Manager.config); },
  draw: function() {
    const manager = this.get('manager');
    const chart = this.get('chart');
    chart.data.labels = manager.get('labels');
    chart.data.datasets = manager.get('datasets');
    chart.update();
  }, //.observes('manager').on('didInsertElement'),
  initialize: function() {
  }.on('didInsertElement'),
  dnitialize: function() {
    this.get('chart').destroy();
  }.on('willDestroyElement')
});
