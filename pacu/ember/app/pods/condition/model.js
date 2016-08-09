import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';

export default Model.extend({
  workspaces: hasMany('workspace'),
  pixel_x: attr(),
  pixel_y: attr(),
  dist: attr(),
  width: attr(),
  height: attr(),
  gamma: attr(),
  on_duration: attr(),
  off_duration: attr(),
  orientations: attr(),
  sfrequencies: attr(),
  tfrequencies: attr(),
  repetition: attr(),
  projection: attr(),
  keyword: attr(),
  on_time: attr(),
  off_time: attr(),
  sequence: attr(),
  ran: attr(),
  order: attr(),
  trial_list: attr()
});
