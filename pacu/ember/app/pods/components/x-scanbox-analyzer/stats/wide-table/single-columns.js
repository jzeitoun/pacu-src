import Ember from 'ember';
import computed, { on } from 'ember-computed-decorators';

export default [
  {
    name: 'Cell ID',
    valuePath: 'id',
  },
  {
    name: 'Anova All F',
    valuePath: 'dtanovaall.value.f',
  },
  {
    name: 'Anova All P',
    valuePath: 'dtanovaall.value.p',
  },
  {
    name: 'SF Cutoff Rel33',
    valuePath: 'dtsfreqfit.value.rc33.0',
  },
  {
    name: 'SF Cutoff Rel33',
    valuePath: 'dtsfreqfit.value.rc33.1',
  },
  {
    name: 'SF Peak',
    valuePath: 'dtsfreqfit.value.peak',
  },
  {
    name: 'SF Pref',
    valuePath: 'dtsfreqfit.value.pref',
  },
  {
    name: 'SF Bandwidth',
    valuePath: 'dtsfreqfit.value.ratio',
  },
  {
    name: 'SF Global OPref',
    valuePath: '',
  }
].map(e => Ember.Object.create(e));
