import Ember from 'ember';
import computed from 'ember-computed-decorators';
import handlers from 'pacu/components/x-andor-device/handlers';

const BASIC_INFOS = [
  'CameraModel', 'ControllerID',
  'FirmwareVersion', 'InterfaceType', // 'SerialNumber',
];
const BASIC_FEATS = [
  'AOIHeight', 'AOIWidth', 'AOIBinning',
];
const BASIC_MODES = [
  'AccumulateCount',
  // 'FrameCount',
  'ExposureTime', 'FrameRate',
  'CycleMode',
  'TriggerMode',
];
  // 'ElectronicShutteringMode',
  // 'AOILeft', 'AOITop',
const ADV_FEATS = [
  'AOIStride', 'Baseline', 'ImageSizeBytes',
  'SensorHeight', 'SensorWidth', 'TimestampClock',
  'TimestampClockFrequency', 'BytesPerPixel', 'MaxInterfaceTransferRate',
  'PixelHeight', 'MetadataEnable', 'MetadataFrame',
  'MetadataTimestamp', 'SensorCooling', 'SpuriousNoiseFilter',
  'StaticBlemishCorrection', 'VerticallyCentreAOI', 'AuxiliaryOutSource',
  'BitDepth', 'EventEnable', 'EventSelector',
  'IOSelector', 'IOInvert', 'PixelEncoding',
  'PixelReadoutRate', 'SimplePreAmpGainControl',
  'SensorTemperature', 'FanSpeed',
  'TemperatureStatus',
  'ReadoutTime',
  'CameraAcquiring', 'FullAOIControl', 'Overlap',
];

export default Ember.Component.extend({
  handlers,
  handlerName: 'bypass',
  busy: false,
  onair: false,
  toast: Ember.inject.service(),
  infos: BASIC_INFOS,
  feats: BASIC_FEATS,
  modes: BASIC_MODES,
  advfs: ADV_FEATS,
  state: '',
  @computed('state') stateStr(s) {
    return s===''   ? 'Initial' :
           s===null ? 'Released':
           s===true ? 'Acquired': 'Unavailable'
  },
  handleError: function(err) {
    this.toast.warning(`${err.title}: ${err.detail}`);
    console.error(err.source.join('\n'));
    throw err;
  },
  streamITV: 30,
  streamOn: false,
  streamModeChanged: function() {
    const streamOn = this.get('streamOn');
    if (streamOn) { this.startStream();
    } else { this.stopStream(); }
  }.observes('streamOn'),
  startStream: function() {
    const self = this;
    (function frame() {
      self.wsx.accessAsBinary('current_frame');
      self.streamID = setTimeout(frame, self.streamITV);
    })();
  },
  stopStream: function() {
    console.log('stop');
    this.streamID = clearTimeout(this.streamID);
  },
  snapStream: function() {
    this.set('streamOn', false);
    this.wsx.accessAsBinary('current_frame');
  },
  cmapNames: ['gray', 'jet', 'hot'],
  actions: {
    setCmap: function(index) {
      const name = this.get('cmapNames')[index];
      this.wsx.invoke('set_cmap', name).then(() => {
        this.toast.info(`Colormap ${name} setup properly.`);
      }).catch(this.handleError.bind(this));
    },
    setHandler: function(name, feats) {
      const args = feats.getEach('value');
      this.wsx.invoke('set_handler', name, ...args).then(() => {
        this.toast.info(`${name.capitalize()} handler setup properly.`);
      }).catch(this.handleError.bind(this));
    },
    selectHandler: function(name) {
      this.set('handlerName', name);
    },
    toggleResource: function() {
      const command = this.get('state') ? 'release_handle' : 'acquire_handle';
      this.wsx.invoke(command).gate('busy').then((state) => {
        this.resetFeatures();
        this.set('state', state);
        this.updateFeatures();
      }).catch(this.handleError.bind(this));
    },
    toggleRecording: function() {
      const command = this.get('onair') ? 'stop_recording' : 'start_recording';
      this.wsx.invoke(command).gate('busy').then((data) => {
        this.set('onair', data);
        this.set('streamOn', data);
      }).catch(this.handleError.bind(this));
    },
    snapCurrentFrame: function() {
      this.snapStream();
    },
    setFeature: function(feature) {
      return this.wsx.invoke(
        'set_feature', feature.key, feature.value
      ).catch(this.handleError.bind(this)).finally(() => {
        this.updateFeatures();
      });
    },
    updateMode: function() {
      const kwargs = {}
      this.modes.forEach((key) => {
        kwargs[this.get(`features.${key}.key`)] = this.get(`features.${key}.value`);
      });
      return this.wsx.invoke(
        'set_features', kwargs
      ).then(() => {
        this.toast.info('Mode changed successfully...');
      }).catch(this.handleError.bind(this)).finally(() => {
        this.updateFeatures();
      });
    },
    setSimpleStreaming: function() {
      this.set('features.AccumulateCount.value', 4); // was 1
      this.set('features.FrameRate.value', 30);
      this.set('features.CycleMode.value', 1); // continue
      this.set('features.ExposureTime.value', 0.01);
      this.set('features.TriggerMode.value', 0); // internal
    },
    setStimulationDriven: function() {
      this.set('features.AccumulateCount.value', 4); // was 1
      this.set('features.FrameRate.value', 30);
      this.set('features.CycleMode.value', 1); // continue
      this.set('features.ExposureTime.value', 0.01);
      this.set('features.TriggerMode.value', 6); //external start
    }
  },
  socket: Ember.inject.service(),
  updateFeatures: function() {
    this.wsx.access('features').then((features) => {
      features.forEach((item) => {
        this.set(`features.${item.feature}`, item);
      });
    });
  },
  resetFeatures: function() {
    this.set('features', {});
  }.on('init'),
  initWS: function() {
    this.wsx = this.get('socket').create(
      this, 'pacu.core.svc.andor', 'AndorBindingService', this.getAttr('src')
    ).then(function(wsx) {
      this.toast.success('WebSocket connection estabilished.');
      wsx.socket.onclose = () => {
        this.toast.warning('WebSocket connection closed.');
      };
    }).onbinary((buf) => {
      this.set('currentBuffer', buf);
    });
    window.qwe = this.wsx;
  }.on('didInsertElement'),
  dnitWS: function() { this.wsx.dnit(); }.on('willDestroyElement'),
  initSUI: function() {
    const self = this;
    this.$('.tabular.menu .item').tab({
      onLoad: function(tabPath, parameterArray, historyEvent) {
        if (Ember.isEqual(tabPath, 'on-air')) {
          self.wsx.invoke('enter_on_air').then(function(msg) {
            if (Ember.isPresent(msg)) {
              self.toast.info(msg);
            }
          }).catch(self.handleError.bind(self));
        } else {
          if (Ember.isEqual(self.prevTabPath, 'on-air')) {
            self.wsx.invoke('exit_on_air').then(function(msg) {
              if (Ember.isPresent(msg)) {
                self.toast.info(msg);
              }
            }).catch(self.handleError.bind(self));
          }
        }
        self.prevTabPath = tabPath;
      }
    });
  }.on('didInsertElement'),
  dnitSUI: function() {
  }.on('willDestroyElement'),
  @computed('features.AOIBinning') sf(feat) {
    return {
      name : feat ? feat.feature : '',
      value: feat ? feat.value : 0,
      items: feat ? feat.range : []
    };
  },
  aoileftchanged: function() {
    const value = this.get('features.AOILeft.value');
    if (Ember.isPresent(this.wsx) && Ember.isPresent(value)) {
      this.wsx.invoke('set_feature', 'aoi_left', value);
    }
  }.observes('features.AOILeft.value'),
  @computed('features.AOILeft') aoileftmin(feat) {
    return feat ? feat.range[0] : 0;
  },
  @computed('features.AOILeft') aoileftmax(feat) {
    return feat ? feat.range[1] : 0;
  },
  aoitopchanged: function() {
    const value = this.get('features.AOITop.value');
    if (Ember.isPresent(this.wsx) && Ember.isPresent(value)) {
      this.wsx.invoke('set_feature', 'aoi_top', value);
    }
  }.observes('features.AOITop.value'),
  @computed('features.AOITop') aoitopmin(feat) {
    return feat ? feat.range[0] : 0;
  },
  @computed('features.AOITop') aoitoptmax(feat) {
    return feat ? feat.range[1] : 0;
  },
  on_sse_notify: function(arg, error) {
    if (error) {
      this.toast.warning(error);
    } else {
      this.toast.info(arg);
    }
  },
});
