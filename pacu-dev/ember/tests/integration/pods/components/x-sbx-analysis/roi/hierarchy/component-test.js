import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-sbx-analysis/roi/hierarchy', 'Integration | Component | x sbx analysis/roi/hierarchy', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{x-sbx-analysis/roi/hierarchy}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#x-sbx-analysis/roi/hierarchy}}
      template block text
    {{/x-sbx-analysis/roi/hierarchy}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
