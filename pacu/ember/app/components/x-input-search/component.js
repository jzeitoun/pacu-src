import Ember from 'ember';

function makeURL(query) {
  return `api/x-input-search/${query}/{query}`;
}
function makeResults(result, id, f1, f2, f3){
  return `
    <a class="result">
      <div class="content">
        <div class="id">#${result[id] || ''}</div>
        <div class="price">${result[f1] || ''}</div>
        <div class="title">${result[f2] || ''}</div>
        <div class="description">${result[f3] || ''}</div>
      </div>
    </a>`;
}
export default Ember.Component.extend({
  classNames: 'ui fluid category search',
  initSUI: function() {
    const self = this;
    const {query, fields, path} = this.getAttr('option');
    const url = makeURL(query);
    this.$().search({
      apiSettings: { url },
      minCharacters: 0,
      type: 'special',
      cache: false,
      templates: {
        special: function(response) {
          const results = response.results.map(
            result => makeResults(result, ...fields)
          ).join('');
          const meta = `<a style="line-height: 0.25em;" class="action">${response.meta.footer}</a>`;
          return meta + results;
        }
      },
      onSelect(result/*, response*/) {
        Ember.set(self.getAttr('field'), 'value', result[path]);
      }
    });
  }.on('didInsertElement'),
  dnitSUI: function() {
    this.$().search('destroy');
  }.on('willDestroyElement')
});
