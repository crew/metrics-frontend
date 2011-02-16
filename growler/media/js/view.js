if(!window.console){
  window.console = {};
  window.console.log = function(){};
}

var labMetrics = {};

labMetrics.tz_offset = new Date().getTimezoneOffset() * 60;

labMetrics.create_chart = function (data) {
  //console.log(data);
  var last
    , start = null
    , i
    , x;
  for (i = 0, l = data.length; i < l; i++) {
    // For new Date(float) the unit is in milliseconds instead of seconds.
    // Account for timezone offset.
    data[i].x = (data[i].timestamp - labMetrics.tz_offset) * 1000;
    data[i].y = data[i].count;
    data[i].name = new Date(data[i].x);
    if (!start) {
      start = data[i].x;
    }
    last = data[i].x;
  }
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
        , width: 800
        , zoomType: 'x'
        }
      // The title.
    , tooltip: {
          formatter: function(){
            var d = new Date(this.x);
            var s = 'There were <b>'+this.y+'</b> computers in use <br/> on: <b>'+
                 (d.getMonth()+1)+'/'+d.getDate()+'/'+d.getFullYear()+'</b> at <b>'+
                 d.getHours()+':'+d.getMinutes()+'</b>';
            return s;
          }
        , shared: true
        }
    , title: {text: ""}
      // The list of "series" (a line you see on the graph).
    , series: [{
          name: "Windows"
        , data: data
        }]
    , xAxis: {
          type: 'datetime'
        , dateTimeLabelFormats: {
              second: '%e %b-%H:%M'
            , minute: '%e %b-%H:%M'
            , hour: '%e %b-%H:%M'
            , day: '%e %b-%H:%M'
            , week: '%e %b-%H:%M'
            , month: '%e %b-%H:%M'
            , year: '%e %b-%H:%M'
            }
        , labels: {
              enabled: true
            , staggerLines: 2
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
}

labMetrics.run = function(jsonViewUrl){
  var start = $('#start')
    , end = $('#end')
    , stime
    , etime
    , now = new Date()
    , dayAgo = new Date(now.getFullYear(), now.getMonth(), now.getDate()-1,
                        now.getHours(), now.getMinutes(), now.getSeconds())
    , ns = "ns";

  start.datetimepicker();
  end.datetimepicker();

  console.log(dayAgo, now)
  start.datetimepicker('setDate', dayAgo);
  end.datetimepicker('setDate', now);

  $("#fetch").click(function (e) {
    $('#fetch').html('<img src="/media/graphics/ajax-loader.gif" %}">');

    e.preventDefault();
    now = new Date();

    stime = start.datetimepicker('getDate');
    etime = end.datetimepicker('getDate');

    if(now - etime < 0) {
      etime = now;
      end.datetimepicker('setDate', now);
    }
    if(now - stime < 0) {
      stime = now;
      start.datetimepicker('setDate', now);
    }
    if(etime - stime < 0) {
      alert('please make sure that the ending date is after the starting date');
      return false;
    }
    else {

      $.ajax({
          type: "GET"
        , url: jsonViewUrl
        , success: labMetrics.create_chart
        , complete: function(){ $('#fetch').html('Fetch'); }
        , data: {
              'ns': ns
            , 'start': stime.getTime()/1000
            , 'end': etime.getTime()/1000
          }
        });
      }
  });

  $('#fetch').click();
}
