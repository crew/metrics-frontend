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
    , reload = $('#reload')
    , intervalId;

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
      window.clearTimeout(intervalId);
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
    labMetrics.reload && intervalId = window.setTimeout(loop, 600000);
  }
  loop();
};
