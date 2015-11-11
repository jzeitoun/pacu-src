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
  acquireResource: function() {
    this.wsx.invoke('acquireResource').then((data) => {
      console.log('resolve then');
      debugger
    }).catch((err) => {
      console.log('resolve catch');
      debugger
    }).finally(() => {
      console.log('resolve fiannyly');
      debugger
    });
  },
  actions: {
    toggleResource: function() {
      this[this.get('state') ? 'releaseResource' : 'acquireResource']();
    },
    reqDebugStream: function() {
      console.log('REQ DBG STRM');
      const self = this;
      function loop() {
        return setTimeout(function() {
          console.log('stream!')
          self.wsx.invokeAsBinary('getDebugFrame');
          self.loopid = loop();
        }, 16);
      };
      self.wsx.invoke('getDebugStream').then(function(data) {
        loop();
        setTimeout(function() {
          console.log('clear!')
          clearTimeout(self.loopid);
          self.wsx.invoke('delDebugStream');
        }, 5000);
      });
    },
    reqTiming: function() {
      console.log('REQ TIMing');
      this.wsx.invoke('getTiming', +(new Date()));
      console.log('REQ SENT!');
    },
    reqDebugFrame: function() {
      console.log('REQ DBG FRM');
      this.wsx.invokeAsBinary('getDebugOneFrame');
      console.log('REQ SENT!');
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
          self.wsx.onbinary(self.setBuffer);
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
    this.wsx = this.get('socket').create(
      this, 'pacu.core.svc.andor', 'AndorBindingService', this.getAttr('src')
    ).then(function(wsx) {
      this.toast.success('WebSocket connection estabilished.');
      wsx.socket.onclose = () => {
        this.toast.warning('WebSocket connection closed.');
      };
    });
    this.$('.tabular.menu .item').tab({
      onLoad: function(tabPath, parameterArray, historyEvent) {}
    });
  }.on('didInsertElement'),
  dnitWS: function() { this.wsx.dnit(); }.on('willDestroyElement'),
});
