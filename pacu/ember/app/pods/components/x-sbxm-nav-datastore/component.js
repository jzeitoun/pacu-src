import Ember from 'ember';
import computed, { on, observes } from 'ember-computed-decorators';

function importRaw(cond) {
  const self = this;
  const modname = 'pacu.core.io.scanbox.impl2';
  const clsname = 'ScanboxIO';
  const $console = Ember.$('#import-progress');
  const messages = this.get('messages');
  const rawName = this.get('activeItem.name');
  const ioPath = [].concat(this.get('arrHops'), rawName + '.io').join('/');
  $console.modal('show', {closable: false});
  this.get('socket').create(this, modname, clsname, {path: ioPath}).then(wsx => {
    messages.pushObject({body: 'Please wait...'});
    wsx.invoke('import_raw', cond).then(newIO => {
      // console.log('IMPORT RAW DONE', newIO);
      this.get('ios').pushObject(newIO);
      this.toast.info(`Data imported successfully.
        Click "New Session" to setup your first analysis.`);
    }).catch(err => {
      self.toast.error(err.detail, err.title);
    }).finally(function() {
      wsx.dnit();
      Ember.run.later(function() {
        $console.modal('hide');
        messages.clear();
      }, 1000);
    });
  });
}

const params = ['hops', 'src', 'glob', 'days'];

export default Ember.Component.extend({
  socket: Ember.inject.service(),
  hops: '',
  filterText: '',
  conditionFilterText: '',
  // nameIn
  // monthPrev
  // src
  //
  classNames: ['ui', 'inverted', 'segment'],
  @on('didInsertElement') initialize() {
    // window.C = this;
    Ember.run.next(this, 'query');
  },
  @observes(...params) query() {
    this.set('busy', true);
    const { hops, src, glob, days } = this.getProperties(params);
    const promise = Ember.$.getJSON(src, { hops, glob, days }).then(data => {
      this.set('dirs', data.dirs);
      this.set('sbxs', data.sbxs);
    }).fail((err, text, statusText) => {
      this.set('err', err);
    }).done(() => {
      this.set('err', null);
    }).always(() => {
      this.set('busy', false);
    });
  },
  @computed() messages() { return []; },
  @computed('hops') arrHops(hops) {
    return hops.split(',').filter(w => !Ember.isEmpty(w));
  },
  @computed('dirs', 'filterText') filteredDIRs(dirs=[], filterText) {
    return dirs.filter(dir => dir.name.includes(filterText));
  },
  @computed('sbxs', 'filterText') filteredSBXs(sbxs=[], filterText) {
    return sbxs.filter(sbx => sbx.name.includes(filterText));
  },
  @computed('conditions', 'conditionFilterText') filteredConds(cs=[], fText) {
    return cs.filterBy('keyword').filter(c => c.keyword.includes(fText));
  },
  actions: {
    popHop() {
      const hops = this.get('arrHops');
      hops.pop();
      this.set('hops', hops.join(','));
    },
    addHop(item) {
      const hops = this.get('arrHops');
      hops.push(item.name);
      this.set('hops', hops.join(','));
    },
    openImportModal(item) {
      this.set('activeItem', item);
      this.toast.info('Search conditions and click to import with the recording.');
      $('.sbx.conditions.modal').modal('show');
    },
    importRawWithCondition(cond) {
      $('.sbx.conditions.modal').modal('hide');
      importRaw.call(this, cond);
    },
    importRawWithoutCondition(cond) {
      $('.sbx.conditions.modal').modal('hide');
      importRaw.call(this);
    }
  },
  on_sse_print(msg, err) {
    if (10 == msg.charCodeAt() || 32 == msg.charCodeAt()) { return; }
    this.get('messages').pushObject({body: msg});
  },
});
