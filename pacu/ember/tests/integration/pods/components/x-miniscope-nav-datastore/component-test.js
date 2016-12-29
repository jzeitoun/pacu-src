import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-miniscope-nav-datastore', 'Integration | Component | x miniscope nav datastore', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{x-miniscope-nav-datastore}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#x-miniscope-nav-datastore}}
      template block text
    {{/x-miniscope-nav-datastore}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
