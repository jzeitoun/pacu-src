import Ember from 'ember';
import computed, { on } from 'ember-computed-decorators';

export default [
  {
    name: 'OSI',
    relPath: 'dtorientationsfits',
    valuePath: 'value.osi',
  },
  {
    name: 'CV',
    relPath: 'dtorientationsfits',
    valuePath: 'value.cv',
  },
  {
    name: 'DSI',
    relPath: 'dtorientationsfits',
    valuePath: 'value.dsi',
  },
  {
    name: 'Sigma',
    relPath: 'dtorientationsfits',
    valuePath: 'value.sigma',
  },
  {
    name: 'OPref',
    relPath: 'dtorientationsfits',
    valuePath: 'value.o_pref',
  },
//   {
//     name: 'Tau',
//     relPath: 'dtorientationsfits',
//     valuePath: 'value.tau',
//   },
  {
    name: 'RMax',
    relPath: 'dtorientationsfits',
    valuePath: 'value.r_max',
  },
  {
    name: 'Residual',
    relPath: 'dtorientationsfits',
    valuePath: 'value.residual',
  },
  {
    name: 'Anova F',
    relPath: 'dtanovaeachs',
    valuePath: 'f',
  },
  {
    name: 'Anova P',
    relPath: 'dtanovaeachs',
    valuePath: 'p',
  }
].map(e => Ember.Object.create(e));
