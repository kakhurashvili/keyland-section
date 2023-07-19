/*======== Google Map chart ========*/
google.charts.load('current', {
  'packages':['geochart'],
});
google.charts.setOnLoadCallback(drawRegionsMap);

function drawRegionsMap() {
  var data = google.visualization.arrayToDataTable([
    ['City', 'Purchased'],

    ['Georgia', 700]

  ]);

  var options = {
colorAxis: {colors: ['#cedbf9', '#6588d5']},
};

  var chart = new google.visualization.GeoChart(document.getElementById('regions_purchase'));

  chart.draw(data, options);
}