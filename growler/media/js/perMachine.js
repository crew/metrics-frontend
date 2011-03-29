labMetrics.create_chart = function (data) {
  var machines = data.machines
    , machinesMap = {}
	  , seriesdata = []
    , seriesdataSsh = null
    , machine
    , series = [];

  function setup(machines, machinesMap, data, seriesdata){
    $.map(machines, function(el, i){
        machinesMap[el] = 0;
    });

    $.map(data, function(el, i){
        machinesMap[el.hostname]++;
    });

    for(machine in machinesMap){
      seriesdata[seriesdata.length] = {name: machine, y: machinesMap[machine]};
    }
  }
    
  if(Array.isArray(data.data)) {
    setup(machines, machinesMap, data.data, seriesdata);
  }
  else {
    setup(machines, machinesMap, data.data.linuxLocal, seriesdata);
    seriesdataSsh = []
    setup(machines, machinesMap, data.data.linuxRemote, seriesdataSsh);
  }
  
  series.push({
          name: seriesdataSsh ? "Linux Local" : "Windows"
        , data: seriesdata
        });
  seriesdataSsh && series.push({
          name: "Linux Remote"
        , data: seriesdataSsh
        });
  
	// Create the chart.
  labMetrics.chart = new Highcharts.Chart({
      chart: {
          defaultSeriesType: "column"
        , marginRight: 25
        , marginBottom: 100
        }
    , series: series
		, xAxis: {
					categories: machines
				,	labels: {
              rotation: -45
            , align: 'right'
						}
			}
    , plotOptions: {
         column: {
            pointPadding: 0.2,
            borderWidth: 0
         }
      }
  });
};
