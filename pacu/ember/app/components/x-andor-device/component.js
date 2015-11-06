import Ember from 'ember';
import computed from 'ember-computed-decorators';

const BASIC_FEATS = [
  'CameraModel',
  'ControllerID',
  'FirmwareVersion',
  'InterfaceType',
  'SerialNumber',
  'AccumulateCount',
  'AOIHeight',
  'AOILeft',
  'AOIStride',
  'AOITop',
  'AOIWidth',
  'Baseline',
  'FrameCount',
  'ImageSizeBytes',
  'SensorHeight',
  'SensorWidth',
  'TimestampClock',
  'TimestampClockFrequency',
  'BytesPerPixel',
  'ExposureTime',
  'FrameRate',
  'MaxInterfaceTransferRate',
  'PixelHeight',
  'ReadoutTime',
  'SensorTemperature',
  'CameraAcquiring',
  'EventEnable',
  'FullAOIControl',
  'IOInvert',
  'MetadataEnable',
  'MetadataFrame',
  'MetadataTimestamp',
  'Overlap',
  'SensorCooling',
  'SpuriousNoiseFilter',
  'StaticBlemishCorrection',
  'VerticallyCentreAOI',
  'AOIBinning',
  'AuxiliaryOutSource',
  'BitDepth',
  'CycleMode',
  'ElectronicShutteringMode',
  'EventSelector',
  'FanSpeed',
  'IOSelector',
  'PixelEncoding',
  'PixelReadoutRate',
  'SimplePreAmpGainControl',
  'TemperatureStatus',
  'TriggerMode',
];

export default Ember.Component.extend({
  feats: BASIC_FEATS,
  state: '',
  @computed('state') stateStr(s) {
    return s===''   ? 'Initial' :
           s===null ? 'Released':
           s===true ? 'Acquired':
                      'Unavailable'
  },
  @computed('state') stateCss(s) { return s===true ? 'block': 'none' },
  actions: {
    setFeature: function(feature) {
      this.wsx.invoke('set_feature', feature);
    },
    acquire: function() {
      const self = this;
      this.wsx.invoke('acquire').then(function(data) {
        if (data.error) {
          alert(data.detail);
        } else {
          self.wsx.mirror('state');
          self.wsx.access('features').then(function(features) {
            features.forEach(function(item) {
              self.set(`features.${item.feature}`, item);
            });
          });
        }
      });
    },
    release: function() {
      const self = this;
      this.wsx.invoke('release').then(function(data) {
        self.set('state', null);
        self.resetFeatures();
      });
    }
  },
  socket: Ember.inject.service(),
  resetFeatures: function() {
    console.log('reset features');
    this.set('features', {});
  }.on('init'),
  initWS: function() {
    window.asd = this;
    const self = this;
    this.wsx = this.get('socket').create(
      this, 'pacu.core.svc.andor', 'AndorBindingService', this.getAttr('src')
    );
    this.$('.tabular.menu .item').tab({
      onLoad: function(tabPath, parameterArray, historyEvent) {}
    });
  }.on('didInsertElement'),
  dnitWS: function() { this.wsx.dnit(); }.on('willDestroyElement'),
});
