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
        , zoomType: 'y'
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
