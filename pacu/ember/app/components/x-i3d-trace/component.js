import Ember from 'ember';

function setupD3(self, trace) {
  var margin = {top: 10, right: 10, bottom: 100, left: 40},
      margin2 = {top: 230, right: 10, bottom: 20, left: 40},
      width = 1024 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom,
      height2 = 300 - margin2.top - margin2.bottom;
  var x = d3.scale.linear().range([0, width]),
      x2 = d3.scale.linear().range([0, width]),
      x3 = d3.scale.linear().range([0, width]),
      y = d3.scale.linear().range([height, 0]),
      y2 = d3.scale.linear().range([height2, 0]);
  var xAxis = d3.svg.axis().scale(x).orient("bottom").innerTickSize(-height),
      xAxis2 = d3.svg.axis().scale(x2).orient("bottom"),
      yAxis = d3.svg.axis().scale(y).orient("left").innerTickSize(-width);
  var brush = d3.svg.brush().x(x2).on("brush", brushed);

  self.x      = x;
  self.x2     = x2;
  self.x3     = x3;
  self.y      = y;
  self.y2     = y2;
  self.xAxis  = xAxis;
  self.xAxis2 = xAxis2;
  self.yAxis  = yAxis;
  self.brush  = brush;

//  var area = d3.svg.area()
//      .interpolate("monotone")
//      .x(function(d) { return x(d.date); })
//      .y0(height)
//      .y1(function(d) { return y(d.price); });
//
//  var area2 = d3.svg.area()
//      .interpolate("monotone")
//      .x(function(d) { return x2(d.date); })
//      .y0(height2)
//      .y1(function(d) { return y2(d.price); });

  self.line = d3.svg.line() // .interpolate("basis")
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.price); });

  self.line2 = d3.svg.line() // .interpolate("basis")
      .x(function(d) { return x2(d.date); })
      .y(function(d) { return y2(d.price); });

  var svg = d3.select(self.element).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom);

  svg.append("defs").append("clipPath")
      .attr("id", "clip")
    .append("rect")
      .attr("width", width)
      .attr("height", height);

  var focus = svg.append("g")
      .attr("class", "focus")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var context = svg.append("g")
      .attr("class", "context")
      .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

  // const data = trace.map(function(e, i) {
  //   return {date: i, price:e}
  // });

  // x.domain([0, data.length]);
  // self.scaleX = x3.domain([0, data.length]);
  // const yMax = d3.max(data.map(function(d) { return d.price; }));
  // const yMin = d3.min(data.map(function(d) { return d.price; }));
  // self.scaleY = y.domain([yMin, yMax]);
  // x2.domain(x.domain());
  // y2.domain(y.domain());

  self.path1 = focus.append("path");
  self.gXAxis = focus.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  self.gYAxis = focus.append("g")
      .attr("class", "y axis")
      .call(yAxis);

  self.path2 = context.append("path");

  self.indexBar = context.append("line")
      .attr("id", "trace-index-bar")
      .attr("x1", 0) //index
      .attr("y1", 0)
      .attr("x2", 0) //index
      .attr("y2", height2)
      .attr("style", "stroke: white;");

  self.gXAxis2 = context.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height2 + ")")
      .call(self.xAxis2);

  context.append("g")
      .attr("class", "x brush")
      .call(brush)
    .selectAll("rect")
      .attr("y", -6)
      .attr("height", height2 + 7);

  function brushed() {
    self.x.domain(self.brush.empty() ? self.x2.domain() : self.brush.extent());
    focus.select(".line").attr("d", self.line);
    focus.select(".x.axis").call(self.xAxis);
  }

}

function updateD3(self, trace) {
  const data = trace.map(function(e, i) {
    return {date: i, price:e}
  });
  self.x.domain([0, data.length]);
  self.scaleX = self.x3.domain([0, data.length]);
  const yMax = d3.max(data.map(function(d) { return d.price; }));
  const yMin = d3.min(data.map(function(d) { return d.price; }));
  self.y.domain([yMin, yMax]);
  self.x2.domain(self.x.domain());
  self.y2.domain(self.y.domain());
  self.path1.datum(data).attr("class", "line").attr("d", self.line);
  self.path2.datum(data).attr("class", "line").attr("d", self.line2);
  self.gYAxis.call(self.yAxis);
  self.gXAxis.call(self.xAxis);
  self.gXAxis2.call(self.xAxis2);
  // self.gBrush.call(self.brush);
}

export default Ember.Component.extend({
  setup: function() {
    setupD3(this);
  }.on('didInsertElement'),
  updateTrace: function() {
    const roi = this.getAttr('currentROI');
    if (Ember.isNone(roi)) {
      this.updateGrandTrace();
    } else {
      console.log(roi.mean);
      if (Ember.isEmpty(roi.mean)) {
        this.toast.warning('Trace is still in fetch. Please wait little more.');
        roi.set('active', false);
      } else {
        updateD3(this, Array.from(roi.mean));
      }
    }
  }.observes('currentROI'),
  updateGrandTrace: function() {
    const trace = this.getAttr('trace');
    updateD3(this, trace);
  }.observes('trace'),
  updateFrame: function() {
    const index = parseInt(this.getAttr('curIndex'));
    this.indexBar.attr('x1', this.scaleX(index)).attr('x2', this.scaleX(index));
  }.observes('curIndex'),
});
