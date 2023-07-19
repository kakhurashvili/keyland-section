/* ====== Index ======

1. RECNT ORDERS
2. USER ACTIVITY
3. ANALYTICS COUNTRY
4. PAGE VIEWS
5. ACTIVITY USER

====== End ======*/
$(function() {
  "use strict";
  
  /*======== 1. RECNT ORDERS ========*/
  if ($("#recent-orders")) {
    var start = moment().subtract(29, "days");
    var end = moment();
    var cb = function(start, end) {
      $("#recent-orders .date-range-report span").html(
        start.format("ll") + " - " + end.format("ll")
      );
    };

    $("#recent-orders .date-range-report").daterangepicker(
      {
        startDate: start,
        endDate: end,
        opens: 'left',
        ranges: {
          Today: [moment(), moment()],
          Yesterday: [
            moment().subtract(1, "days"),
            moment().subtract(1, "days")
          ],
          "Last 7 Days": [moment().subtract(6, "days"), moment()],
          "Last 30 Days": [moment().subtract(29, "days"), moment()],
          "This Month": [moment().startOf("month"), moment().endOf("month")],
          "Last Month": [
            moment()
              .subtract(1, "month")
              .startOf("month"),
            moment()
              .subtract(1, "month")
              .endOf("month")
          ]
        }
      },
      cb
    );
    cb(start, end);
  }

 /*======== 2. USER ACTIVITY ========*/
if ($("#user-activity")) {
  var start = moment().subtract(1, "days");
  var end = moment().subtract(1, "days");
  var cb = function(start, end) {
    $("#user-activity .date-range-report span").html(
      start.format("ll") + " - " + end.format("ll")
    );
    
    // Call the function to get user activity data based on the new dates
    get_user_activity_data(start.format("YYYY-MM-DD"), end.format("YYYY-MM-DD"))
      .then(function(activityData) {
        // Process the activity data and display active and inactive times
        displayUserActivityTimes(activityData);
      })
      .catch(function(error) {
        console.error("Error retrieving user activity data:", error);
      });
  };

  $("#user-activity .date-range-report").daterangepicker(
    {
      startDate: start,
      endDate: end,
      opens: 'left',
      ranges: {
        Today: [moment(), moment()],
        Yesterday: [
          moment().subtract(1, "days"),
          moment().subtract(1, "days")
        ],
        "Last 7 Days": [moment().subtract(6, "days"), moment()],
        "Last 30 Days": [moment().subtract(29, "days"), moment()],
        "This Month": [moment().startOf("month"), moment().endOf("month")],
        "Last Month": [
          moment()
            .subtract(1, "month")
            .startOf("month"),
          moment()
            .subtract(1, "month")
            .endOf("month")
        ]
      }
    },
    cb
  );
  cb(start, end);
}

// Define a function to display user activity times
function displayUserActivityTimes(activityData) {
  // Clear previous data
  $("#user-activity .active-times").empty();
  $("#user-activity .inactive-times").empty();

  // Iterate through the activityData and display active and inactive times
  activityData.forEach(function(data) {
    var dateLabel = data.date_label;
    var activeTimes = data.active_times;
    var inactiveTimes = data.inactive_times;

    // Display active times
    var activeTimesHtml = "<strong>" + dateLabel + "</strong>: " + activeTimes.join(", ");
    $("#user-activity .active-times").append("<li>" + activeTimesHtml + "</li>");

    // Display inactive times
    var inactiveTimesHtml = "<strong>" + dateLabel + "</strong>: " + inactiveTimes.join(", ");
    $("#user-activity .inactive-times").append("<li>" + inactiveTimesHtml + "</li>");
  });
}

// Function to get user activity data based on the provided start date and end date
function get_user_activity_data(startDate, endDate) {
  // Make an AJAX request or fetch API call to retrieve the user activity data from the server
  // based on the provided start date and end date
  // Return the retrieved data or process it as needed

  // Example implementation:
  return fetch("/admin?start_date=" + startDate + "&end_date=" + endDate)
    .then(response => response.json())
    .then(data => data.activityData);
}

// Function to update the user activity times
// Update the user activity times
// Function to update the date range report
function updateDateRange(startDate, endDate) {
  var dateRangeElement = document.getElementById("date-range");
  if (dateRangeElement) {
    var startDateFormatted = moment(startDate).format("MMM D, YYYY");
    var endDateFormatted = moment(endDate).format("MMM D, YYYY");
    var dateRangeText = startDateFormatted + " - " + endDateFormatted;
    dateRangeElement.textContent = dateRangeText;
  }
}

// Update the date range
function updateActivityTimes() {
  var startDate = moment(document.getElementById("start-date").value, "YYYY-MM-DD");
  var endDate = moment(document.getElementById("end-date").value, "YYYY-MM-DD");

  // Check if the dates are valid
  if (startDate.isValid() && endDate.isValid()) {
    // Call the function to update the date range report
    updateDateRange(startDate, endDate);
  } else {
    console.error("Invalid date - Invalid date");
  }
}

// Add an event listener to the date range input fields
document.getElementById("start-date").addEventListener("change", updateActivityTimes);
document.getElementById("end-date").addEventListener("change", updateActivityTimes);



// Event listener for date range change
$('.date-range-picker').on('apply.daterangepicker', function(ev, picker) {
  // Update the user activity times
  updateActivityTimes();
});

// Initial update of user activity times
updateActivityTimes();


// Set an event listener to update the user activity times when the date range is changed
$("#user-activity .date-range-report").on("apply.daterangepicker", updateActivityTimes);


  /*======== 3. ANALYTICS COUNTRY ========*/
  if ($("#analytics-country")) {
    var start = moment();
    var end = moment();
    var cb = function(start, end) {
      $("#analytics-country .date-range-report span").html(
        start.format("ll") + " - " + end.format("ll")
      );
    };

    $("#analytics-country .date-range-report").daterangepicker(
      {
        startDate: start,
        endDate: end,
        opens: 'left',
        ranges: {
          Today: [moment(), moment()],
          Yesterday: [
            moment().subtract(1, "days"),
            moment().subtract(1, "days")
          ],
          "Last 7 Days": [moment().subtract(6, "days"), moment()],
          "Last 30 Days": [moment().subtract(29, "days"), moment()],
          "This Month": [moment().startOf("month"), moment().endOf("month")],
          "Last Month": [
            moment()
              .subtract(1, "month")
              .startOf("month"),
            moment()
              .subtract(1, "month")
              .endOf("month")
          ]
        }
      },
      cb
    );
    cb(start, end);
  }

  /*======== 4. PAGE VIEWS ========*/
  if ($("#page-views")) {
    var start = moment();
    var end = moment();
    var cb = function(start, end) {
      $("#page-views .date-range-report span").html(
        start.format("ll") + " - " + end.format("ll")
      );
    };

    $("#page-views .date-range-report").daterangepicker(
      {
        startDate: start,
        endDate: end,
        opens: 'left',
        ranges: {
          Today: [moment(), moment()],
          Yesterday: [
            moment().subtract(1, "days"),
            moment().subtract(1, "days")
          ],
          "Last 7 Days": [moment().subtract(6, "days"), moment()],
          "Last 30 Days": [moment().subtract(29, "days"), moment()],
          "This Month": [moment().startOf("month"), moment().endOf("month")],
          "Last Month": [
            moment()
              .subtract(1, "month")
              .startOf("month"),
            moment()
              .subtract(1, "month")
              .endOf("month")
          ]
        }
      },
      cb
    );
    cb(start, end);
  }
  /*======== 5. ACTIVITY USER ========*/
  if ($("#activity-user")) {
    var start = moment();
    var end = moment();
    var cb = function(start, end) {
      $("#activity-user .date-range-report span").html(
        start.format("ll") + " - " + end.format("ll")
      );
    };

    $("#activity-user .date-range-report").daterangepicker(
      {
        startDate: start,
        endDate: end,
        opens: 'left',
        ranges: {
          Today: [moment(), moment()],
          Yesterday: [
            moment().subtract(1, "days"),
            moment().subtract(1, "days")
          ],
          "Last 7 Days": [moment().subtract(6, "days"), moment()],
          "Last 30 Days": [moment().subtract(29, "days"), moment()],
          "This Month": [moment().startOf("month"), moment().endOf("month")],
          "Last Month": [
            moment()
              .subtract(1, "month")
              .startOf("month"),
            moment()
              .subtract(1, "month")
              .endOf("month")
          ]
        }
      },
      cb
    );
    cb(start, end);
  }
});
