import Ember from 'ember';
import computed from 'ember-computed-decorators';

const BASIC_INFOS = [
  'CameraModel',
  'ControllerID',
  'FirmwareVersion',
  'InterfaceType',
  'SerialNumber',
];
const BASIC_FEATS = [
  'AccumulateCount',
  'AOIHeight',
  'AOILeft',
  'AOITop',
  'AOIWidth',
  'FrameCount',
  'ExposureTime',
  'FrameRate',
  'AOIBinning',
];
const ADV_FEATS = [
  'AOIStride',
  'Baseline',
  'ImageSizeBytes',
  'SensorHeight',
  'SensorWidth',
  'TimestampClock',
  'TimestampClockFrequency',
  'BytesPerPixel',
  'MaxInterfaceTransferRate',
  'PixelHeight',
  'MetadataEnable',
  'MetadataFrame',
  'MetadataTimestamp',
  'SensorCooling',
  'SpuriousNoiseFilter',
  'StaticBlemishCorrection',
  'VerticallyCentreAOI',
  'AuxiliaryOutSource',
  'BitDepth',
  'EventEnable',
  'EventSelector',
  'IOSelector',
  'IOInvert',
  'PixelEncoding',
  'PixelReadoutRate',
  'SimplePreAmpGainControl',
  'CycleMode',
  'ElectronicShutteringMode',
  'SensorTemperature',
  'FanSpeed',
  'TemperatureStatus',
  'TriggerMode',
  'ReadoutTime',
  'CameraAcquiring',
  'FullAOIControl',
  'Overlap',
];

export default Ember.Component.extend({
  busy: false,
  toast: Ember.inject.service(),
  infos: BASIC_INFOS,
  feats: BASIC_FEATS,
  advfs: ADV_FEATS,
  state: '',
  @computed('state') stateStr(s) {
    return s===''   ? 'Initial' :
           s===null ? 'Released':
           s===true ? 'Acquired':
                      'Unavailable'
  },
  @computed('state') stateCss(s) { return s===true ? 'block': 'none' },
  setBuffer(buf) {
    console.log('set buffer -> currentBuffer');
    this.set('currentBuffer', buf);
  },
  actions: {
    reqDebugFrame: function() {
      console.log('REQ DBG FRM');
      this.wsx.onbinary(this.setBuffer).invokeAsBinary('getDebugFrame');
    },
    setFeature: function(feature) {
      return this.wsx.invoke('set_feature', feature);
    },
    acquire: function() {
      const self = this;
      self.set('busy', true);
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
        self.set('busy', false);
      });
    },
    release: function() {
      const self = this;
      self.set('busy', true);
      this.wsx.invoke('release').then(function(data) {
        self.set('state', null);
        self.set('busy', false);
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
