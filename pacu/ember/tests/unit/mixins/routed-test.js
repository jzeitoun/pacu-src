import Ember from 'ember';
import RoutedMixin from 'pacu/mixins/routed';
import { module, test } from 'qunit';

module('Unit | Mixin | routed');

// Replace this with your real tests.
test('it works', function(assert) {
  let RoutedObject = Ember.Object.extend(RoutedMixin);
  let subject = RoutedObject.create();
  assert.ok(subject);
});
