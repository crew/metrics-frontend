labMetrics.create_chart = function (givendata) {
  var last
    , start = null
    , i
    , x
    , windowsdata = []
    , linuxLocal = []
    , linuxRemote = []
    , linuxBoth = []
    , tenmins = 60*10*1000;

  function milliseconds(data, givendata, name){
    $.map(givendata, function(el, i){
        var time = (givendata[i].timestamp - labMetrics.tz_offset) * 1000
          , current = {};

        current.x = time;
        current.y = givendata[i].count;
        current.name = name;//new Date(time);

        if (!start) {
          start = current.x;
        }
        last = current.x
        data[data.length] = current;
    });
  }
  milliseconds(windowsdata, givendata.windows, 'Windows');
  milliseconds(linuxLocal, givendata.linux.local, 'Linux Local');
  milliseconds(linuxRemote, givendata.linux.ssh, 'Linux Remote');

  var offset = 0;
  $.map(linuxLocal, function(el, i){
    if(linuxRemote[i+offset] && el.x == linuxRemote[i+offset].x) {
      var current = {};
      
      current.x = el.x;
      current.y = el.y + (linuxRemote[i] ? linuxRemote[i+offset].y : 0);
      current.name = 'Linux Total'
      linuxBoth[linuxBoth.length] = current;
    }
    else {
      offset++
    }

    return el;
  });

  console.log(linuxBoth[0], linuxLocal[0], linuxRemote[0]);

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
            var windows, linux, p, d, i, l, s;

            d = new Date(this.x);
            s = d.toString().split(' GMT')[0];

            for(i = 0, l = this.points.length; i < l; ++i){
              p = this.points[i].point;
              s += '<br>'+p.name+': <b>'+p.y+'</b>'
            }
            return s;
          }
        , shared: true
        }
    , title: {text: ""}
      // The list of "series" (a line you see on the graph).
    , series: [{
          name: "Windows"
        , data: windowsdata
        }
        , {
            name: "Linux Total"
          , data: linuxBoth
        }
        , {
            name: "Linux Local"
          , data: linuxLocal
        }
        , {
            name: "Linux Remote"
          , data: linuxRemote
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
