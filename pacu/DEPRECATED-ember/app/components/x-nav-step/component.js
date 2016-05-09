import Ember from 'ember';

/* global Mousetrap */
/* global jQuery */

const enter = jQuery.Event('keydown', { which: 13 });
const arrowup = jQuery.Event('keydown', { which: 38 });
const arrowdn = jQuery.Event('keydown', { which: 40 });

function bindKey(self, elem, stroke, event) {
  Mousetrap(elem).bind(stroke, (/*e*/) => {
    self.$().trigger(event);
    return false;
  });
}

export default Ember.Component.extend({
  classNames: 'ui fluid multiple search selection dropdown',
  classNameBindings: ['busy:loading', 'broke:error'],
  broken: false,
  busy: false,
  defaultText: 'Please select or type to navigate...',
  lastLabel: null,
  initSUI: function() {
    const self = this;
    self.$().on('click', 'i.check', function() {
      self.select();
    });
    self.$().dropdown({
      match: 'value',
      fullTextSearch: true,
      // action: 'combo',
      action: function(text, value) {
        if (Ember.isEmpty(value)) { return; } else {
          jQuery(self.element).dropdown('set selected', value, jQuery(this));
        }
      },
      // onLabelSelect($selectedLabels)
      onAdd: function(/*addedValue, addedText, $addedChoice*/) {
        // handle with file item which should block everything except
        // backspace and enter
      },
      onChange: function(value/*, text, $selectedItem*/) {
        const arg = arguments;
        self.$().dropdown('hide');
        self.set('content', []);
        const hops = value.split(',');
        self.attrs.value.update(hops);
        self.fetchSteps(...hops).done(() => {
          if (self.get('canSelect')) {
            self.$('a:last')
              .addClass('can-select')
              .append($('<i>', {class:'check icon'}));
          }
          Ember.run.next(self.$(), 'dropdown', 'show');
        });
      }
    });
    bindKey(self, self.element, 'ctrl+p', arrowup);
    bindKey(self, self.element, 'ctrl+n', arrowdn);
    Mousetrap(self.element).bind('enter', (/*e*/) => {
      self.select();
      return false;
    });
    const src = self.getAttr('src');
    const val = self.get('attrs.value.update');
    if (Ember.isNone(src)) {
      return self.breakdown(
        'Could not find `src` attribute on component definition.');
    }
    if (Ember.isNone(val)) {
      return self.breakdown(
        'Could not find `value` attribute or it is not a property type.');
    }
    Ember.run.schedule('afterRender', self, 'fetchSteps');
  }.on('didInsertElement'),
  select: function() {
    const self = this;
    if (self.get('canSelect')) {
      self.fetchAction('select').done((json) => {
        self.attrs.selected.update(json.data);
        Ember.run.next(self.$(), 'dropdown', 'hide');
        Ember.run.next(self, 'sendAction', 'onSelect');
      });
    }
  },
  dnitSUI: function() {
    this.$().dropdown('destroy');
    Mousetrap(this.element).unbind(['ctrl+p', 'ctrl+n', 'enter']);
    self.$().off('click', 'i.check');
  }.on('willDestroyElement'),
  breakdown(msg) {
    Ember.run.schedule('afterRender', this, () => {
      this.set('defaultText', msg);
      this.set('broke', true);
    });
  },
  remoteActions: [],
  canSelect: function() {
    return this.get('remoteActions').contains('select');
  }.property('remoteActions'),
  stack: [],
  fetchAction(action) {
    const hops = this.getAttr('value');
    const src = [].concat(this.getAttr('src'), ...hops).filter(e => !!e).join('/');
    return Ember.$.getJSON(src, {action}) ; //.done((json) => { console.log(json); });
  },
  fetchSteps(...hops) {
    const self = this;
    self.set('busy', true);
    const src = [].concat(self.getAttr('src'), ...hops).filter(e => !!e).join('/');
    const req = Ember.$.getJSON(src).done((json) => {
      if (self.stack.length == 1) {
        self.set('remoteActions', json.actions);
        self.set('content', json.data);
      }
    }).fail((xhr, status, error) => {
      self.breakdown(`Error in fetching resources: ${status}`);
      console.error(error);
    }).always((xhr) => {
      self.stack.shift();
      if (Ember.isEmpty(self.stack)) {
        self.set('busy', false);
      }
    });
    this.stack.push(req);
    return req;
  }
});
