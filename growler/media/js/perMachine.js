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
      chart: {
          defaultSeriesType: "column"
        , marginRight: 25
        , marginBottom: 100
        }
    , series: [{
          name: "Windows"
        , data: seriesdata
        }]
		, xAxis: {
					categories: machines
				,	labels: {
              rotation: -45
            , align: 'right'
						}
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
  });
};
