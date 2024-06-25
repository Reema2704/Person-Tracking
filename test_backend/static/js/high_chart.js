// script.js
document.addEventListener("DOMContentLoaded", function () {
    fetch("/tracks/get_all")
        .then((response) => response.json())
        .then((data) => {
            createChart(data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});

function uuidToNumber(uuid) {
    // Implement your UUID to numeric conversion logic here
    // For simplicity, let's assume it returns a random number between 0 and 100
    return Math.random() * 100;
  }

function createChart(data) {
    console.log(data);
    // Process the data to prepare it for the Highcharts chart
    Highcharts.chart('lineChartContainer', {
        chart: {
          type: 'line'
        },
        title: {
          text: 'Line Chart: Timestamp vs Camera ID with Person ID'
        },
        xAxis: {
          type: 'datetime',
          title: {
            text: 'Timestamp'
          }
        },
        yAxis: {
          type:'text',
          title: {
            text: 'Camera ID (UUID to Number)'
          }
        },
        // tooltip: {
        //   formatter: function () {
        //     return `Camera ID: ${this.point.cameraId}<br>Person ID: ${Object.keys(personIds).find(key => personIds[key] === this.y)}`;
        //   }
        // },
        series: Object.keys(data).map(person_id => ({
          name: person_id,
          data: data[person_id],
        }))
      })
    }



// document.addEventListener("DOMContentLoaded", function() {
//   // Given data
//   const rawData = {
//       "64c2a69b17b807b1e628629c": [["2023-07-27T01:59:27.121515","1"],["2023-07-27T01:59:27.121530","2"],["2023-07-27T01:59:27.121540","3"]],
//       "64c2a6a117b807b1e628629e": [["2023-07-27T01:59:27.121515","2"],["2023-07-27T01:59:27.121520","1"],["2023-07-27T01:59:27.12151540","3"]]
//   };

//   // Convert timestamp strings to JavaScript Date objects
//   const data = {};
//   for (const [personId, entries] of Object.entries(rawData)) {
//       data[personId] = entries.map(entry => [new Date(entry[0]).getTime(), parseInt(entry[1])]);
//   }

//   // Create the Highchart
//   Highcharts.chart('chart-container', {
//       chart: {
//           type: 'line'
//       },
//       title: {
//           text: 'Highchart for Data'
//       },
//       xAxis: {
//           type: 'datetime',
//           title: {
//               text: 'Timestamp'
//           }
//       },
//       yAxis: {
//           title: {
//               text: 'Value'
//           }
//       },
//       series: Object.entries(data).map(([personId, seriesData]) => ({
//           name: personId,
//           data: seriesData
//       }))
//   });
// });