import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-i3d2p-plot-overview', 'Integration | Component | x i3d2p plot overview', {
  integration: true
});

test('it renders', function(assert) {
  assert.expect(2);

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{x-i3d2p-plot-overview}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#x-i3d2p-plot-overview}}
      template block text
    {{/x-i3d2p-plot-overview}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
