import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-trj-analysis/mouse-trajectory', 'Integration | Component | x trj analysis/mouse trajectory', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });"

  this.render(hbs`{{x-trj-analysis/mouse-trajectory}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:"
  this.render(hbs`
    {{#x-trj-analysis/mouse-trajectory}}
      template block text
    {{/x-trj-analysis/mouse-trajectory}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
