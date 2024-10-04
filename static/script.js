// Function to fetch data from the server
function fetchData() {
    const mis = $('#misInput').val();  // Get the MIS number from input
    $.ajax({
        type: 'POST',
        url: '/fetch_data',  // URL to send the POST request
        contentType: 'application/json',  // Specify the content type
        data: JSON.stringify({ mis: mis }),  // Send the MIS number as JSON
        success: function(response) {
            // Clear previous results
            $('#resultsTable thead').empty();
            $('#resultsTable tbody').empty();

            // Generate table headers dynamically
            const columns = response.columns;  // Get column names from response
            const headerRow = '<tr>' + columns.map(col => `<th>${col}</th>`).join('') + '</tr>';
            $('#resultsTable thead').append(headerRow);

            // Populate table with new results
            response.data.forEach(row => {
                const rowHtml = '<tr>' + columns.map(col => `<td>${row[col]}</td>`).join('') + '</tr>'; // Ensure rows correspond to columns
                $('#resultsTable tbody').append(rowHtml);
            });
        },
        error: function(error) {
            console.log("Error fetching data:", error);  // Log any errors
        }
    });
}

