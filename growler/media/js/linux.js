Highcharts.setOptions({
    legend: {
        align: 'right'
      , enabled: true
      , x: -100
      , verticalAlign: 'top'
      , y: 20
      , floating: true
      , backgroundColor: Highcharts.theme.legendBackgroundColorSolid || '#FFFFFF'
      , borderColor: '#CCC'
      , borderWidth: 1
      , shadow: false
    }
  , tooltip: {
         formatter: function() {
            console.log(this);
            return '<b>'+ this.x +'</b><br/>'+
                this.series.name +': '+ this.y +'<br/>'+
                'Total: '+ this.point.stackTotal;
         }
    }
  , yAxis: {
      title: {
          text: 'Total Number of logins'
      }
    }
  , plotOptions: {
        column: {
            stacking: 'normal'
        }
    }
});
