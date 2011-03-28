Highcharts.setOptions({
    credits: {text: "crew", href: "."}
  , chart: {
        // the id of the div element for drawing the graph.
        renderTo: "graph"
        // The type of the graph.
      , defaultSeriesType: "line"
      , marginRight: 170
      , marginBottom: 100
      , width: 980
      }
  , title: {text: ""}
    , xAxis: {
          labels: {
              enabled: true
            //, staggerLines: 2
            , rotation: -45
            , align: 'right'
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
