labMetrics.create_chart = function (givendata) {
  var last
    , start = null
    , i
    , x
    , data = []
    , tenmins = 60*10*1000;

  //for (i = 0, l = data.length; i < l; i++) {
    // For new Date(float) the unit is in milliseconds instead of seconds.
    // Account for timezone offset.
  $.map(givendata, function(el, i){
      var time = (givendata[i].timestamp - labMetrics.tz_offset) * 1000
        , current = {};

      current.x = time;
      current.y = givendata[i].count;
      current.name = new Date(time);

      if (!start) {
        start = current.x;
      }
      last = current.x
      data[data.length] = current;
  });

  // Create the chart.
  labMetrics.chart = new Highcharts.Chart({
      credits: {text: "crew", href: "."}
    , chart: {
          // the id of the div element for drawing the graph.
          renderTo: "graph"
          // The type of the graph.
        , defaultSeriesType: "line"
        , marginRight: 170
        , marginBottom: 100
        , width: 980
        , zoomType: 'x'
        }
      // The title.
    , tooltip: {
          formatter: function(){
            var windows, linux, d, i, l, s;
            for(i = 0, l = this.points.length; i < l; ++i){
              if(this.points[i].point.name == 'windows') windows = this.points[i];
              else if(this.points[i].point.name == 'linux') linux = this.points[i];
            }
            d = new Date(this.x);
            s = d.toString().split(' GMT')[0] +
                (linux ? '<br>Linux: <b>'+linux.y+'</b>' : '') +
                (windows ? '<br>Windows: <b>'+windows.y+'</b>' : '');
            return s;
          }
        , shared: true
        }
    , title: {text: ""}
      // The list of "series" (a line you see on the graph).
    , series: [{
          name: "Windows"
        , data: $.map(data, function(el, i){ return $.extend(true, {}, el, {name: 'windows'});})
        }
        , {
            name: "Linux"
          , data: $.map(data, function(el, i){
                return $.extend(true, {}, el, {name: 'linux', y: 0/*~~((5/2)*el.y)*/});
            })
        }]
    , xAxis: {
          type: 'datetime'
        , labels: {
              enabled: true
            //, staggerLines: 2
            , rotation: -45
            , align: 'right'
            , formatter: function(){
                var d = new Date(this.value);
                return ''+Highcharts.dateFormat('%d %b', d)+'-'+
                  ('0'+d.getHours()).slice(-2)+':'+('0'+d.getMinutes()).slice(-2);
            }
          }
        }
    , yAxis: {
          title: {
              text: 'Computers In Use'
        }
        , plotLines: [{
              value: 0
            , width: 1
            , color: '#808080'
        }]
      }
    , legend: {
          align: 'right'
        , borderWidth: 0
        , layout: 'vertrical'
        , verticalAlign: 'middle'
        , x : -15
      }
    , plotOptions: {
        line: {
          pointStart: start
        }
      }
    , exporting: {
          enabled: true
        }
  });
};
