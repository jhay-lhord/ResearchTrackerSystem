    "use strict"
  // fetch data from back end
  console.log("running")
  const research_data = JSON.parse("{{research_data_json|escapejs}}");
  const mixedChart1 = document.querySelector("#mixed-chart-1");

  const labelss = research_data.labels.reverse();

  if (mixedChart1 !== null) {
    var mixedOptions1 = {
      chart: {
        height: 370,
        type: "bar",
        toolbar: {
          show: false,
        },
      },
      colors: ["#fd5190", "#0acb8e", "#9e6de0", "#04c7e0"],
      legend: {
        show: true,
        position: "top",
        horizontalAlign: "right",
        markers: {
          width: 20,
          height: 5,
          radius: 0,
        },
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: "50%",
          barHeight: "10%",
          distributed: false,
        },
      },
      dataLabels: {
        enabled: false,
      },

      stroke: {
        show: true,
        width: 2,
        curve: "smooth",
      },

      series: [
        {
          name: "On-Going",
          type: "column",
          data:research_data.ongoing,
        },
        {
          name: "Conducted",
          type: "column",
          data: research_data.conducted,
        },
        {
          name: "Presented",
          data: research_data.presented,
          type: "column",
        },
        {
          name: "Published",
          data: research_data.published,
          type: "column",
        },
      ],

      xaxis: {
        categories: labelss,
        // categories: ["June", "July", "August", "September", "October"],

        axisBorder: {
          show: false,
        },
        axisTicks: {
          show: false,
        },
        crosshairs: {
          width: 40,
        },
      },

      fill: {
        opacity: 1,
      },

      tooltip: {
        shared: true,
        intersect: false,
        followCursor: true,
        fixed: {
          enabled: false,
        },
        x: {
          show: false,
        },
        y: {
          title: {
            formatter: function (seriesName) {
              return seriesName;
            },
          },
        },
      },
    };

    var randerMixedChart1 = new ApexCharts(mixedChart1, mixedOptions1);
    randerMixedChart1.render();
  }
