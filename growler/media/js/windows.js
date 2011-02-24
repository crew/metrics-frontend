if(!window.console){
  window.console = {};
  window.console.log = function(){};
}

var labMetrics = {};

labMetrics.tz_offset = new Date().getTimezoneOffset() * 60;
labMetrics.reload = true;

labMetrics.getLast24 = function(){
  var now = new Date()
    , dayAgo = new Date(now.getFullYear(), now.getMonth(), now.getDate()-1,
                        now.getHours(), now.getMinutes(), now.getSeconds())

  return {
      now: now
    , dayAgo: dayAgo
    };
};

labMetrics.create_chart = function (data) {
  var machines = data.machines
    , machinesMap = {}
	  , seriesdata = []
    , machine;
    
  $.map(machines, function(el, i){
      machinesMap[el] = 0;
	});

  $.map(data.data, function(el, i){
      machinesMap[el.hostname]++;
      if(isNaN(machinesMap[el.hostname])){
        debugger;
      }
  });

  for(machine in machinesMap){
    seriesdata[seriesdata.length] = {name: machine, y: machinesMap[machine]};
  }
  
	// Create the chart.
  labMetrics.chart = new Highcharts.Chart({
      credits: {text: "crew", href: "."}
    , chart: {
          // the id of the div element for drawing the graph.
          renderTo: "graph"
          // The type of the graph.
        , defaultSeriesType: "column"
        , marginRight: 25
        , marginBottom: 100
        , width: 980
        }
      // The title.
    , title: {text: ""}
      // The list of "series" (a line you see on the graph).
    , series: [{
          name: "Windows"
        , data: seriesdata
        }]
		, xAxis: {
					categories: machines
				,	labels: {
              rotation: -45
						//,	staggerLines: 3
            , align: 'right'
						}
			}
    , yAxis: {
          title: {
              text: 'Total Usage'
        }
        , plotLines: [{
              value: 0
            , width: 1
            , color: '#808080'
        }]
      }
    , legend: {
				enabled: false
      }
    , plotOptions: {
         column: {
            pointPadding: 0.2,
            borderWidth: 0
         }
      }
    , exporting: {
          enabled: true
        }
  });
};

labMetrics.reloadChart = function(start, end){
  var stime
    , etime
    , ns = "windows";

  start && labMetrics.start.datetimepicker('setDate', start);
  end && labMetrics.end.datetimepicker('setDate', end);

  var now = new Date();

  stime = labMetrics.start.datetimepicker('getDate');
  etime = labMetrics.end.datetimepicker('getDate');

  if(now - etime < 0) {
    etime = now;
    labMetrics.end.datetimepicker('setDate', now);
  }
  if(now - stime < 0) {
    stime = now;
    labMetrics.start.datetimepicker('setDate', now);
  }
  if(etime - stime < 0) {
    alert('please make sure that the ending date is after the starting date');
    return false;
  }
  else {

    $('#fetch').html('<img src="/media/graphics/ajax-loader.gif">');

    $.ajax({
        type: "GET"
      , url: labMetrics.jsonViewUrl
      , success: labMetrics.create_chart
      , complete: function(){ $('#fetch').html('Fetch'); }
      , data: {
            'ns': ns
          , 'start': stime.getTime()/1000
          , 'end': etime.getTime()/1000
        }
      });
    }
};

labMetrics.run = function(jsonViewUrl){
  var last24 = labMetrics.getLast24()
    , reload = $('#reload');

  labMetrics.jsonViewUrl = jsonViewUrl;

  labMetrics.start = $('#start');
  labMetrics.end = $('#end');

  labMetrics.start.datetimepicker({
      onClose: function(){ $('#fetch').click(); }
    });
  labMetrics.end.datetimepicker({
      onClose: function(){ $('#fetch').click(); }
    });

  reload.click(function(e) {
    if(labMetrics.reload) {
      labMetrics.reload = false;
      reload.html('Auto Reloading OFF.');
    }
    else {
      labMetrics.reload = true;
      reload.html('Auto Reloading ON.');
      loop();
    }
  });

  $("#fetch").click(function (e) {
      e.preventDefault();
      labMetrics.reload && reload.click();
      labMetrics.reloadChart();
  });


  function loop(){
    var last24 = labMetrics.getLast24();
    labMetrics.reloadChart(last24.dayAgo, last24.now);

    labMetrics.reload && setTimeout(loop, 600000);
  }
  loop();
};
