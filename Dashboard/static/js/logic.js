// Global variables
user_data = []
activity_data = []

// Get all user IDs
let users_url = "http://127.0.0.1:5000/api/v1.0/users"
d3.json(users_url).then(function(ids){
    // Add the ids to the dropdown menu
    let dropDownMenu = d3.select("#selDataset");
    
    // Loop through the samples
    for (let i=0; i<ids.length; i++){
        // Add the sample id to the dropdown menu
        dropDownMenu.append("option").attr("value", ids[i]).text(ids[i]);
    }

    // Get all data for one user
    let dropDownMenuValue = d3.select("#selDataset").property("value");
    optionChanged(dropDownMenuValue);
});


function displayDemoInfo(user_data) {
// Display the demographic info in the text box
    d3.select("#sample-metadata-datapoints").text(`data points: ${user_data.length}`);
    d3.select("#sample-metadata-start").text(`start date: ${user_data[0].ActivityDate}`);
    d3.select("#sample-metadata-last").text(`last date: ${user_data[user_data.length-1].ActivityDate}`);
}

function optionChanged(value) {
// Event listener. Update the dashboard when the dropdown menu is used
    let user_data_url = `http://127.0.0.1:5000/api/v1.0/u/${value}`
    d3.json(user_data_url).then(function(data){
        // Add the ids to the dropdown menu
        user_data = data;
    });
    displayDemoInfo(user_data);

    // Update the gauge
    //displayGauge(info.wfreq)

    // Update the charts
    //let sample = getSampleById(samples, value);
    displayHBar(user_data);
    //displayBubbleChart(sample);
}

// $.getJSON(url, function(json) {
//     console.log( "JSON Data: " + json);
//    });

function displayHBar(samples) {
    // Display horizontal bar chart for top 10 otu ids
    
        // Combine the arrays into a single object
        // Prototype: [{otu_ids: ..., sample_values: ...}, {...}, {...}]
        let samples_list = [];
        for (let i=0; i<samples.length;i++) {
            samples_list.push({
                date: samples[i].TotalSteps,
                steps: samples[i].ActivityDate
            });
        }

        console.log(samples_list)
        
        // Trace for the OTU data
        let trace = {
            x: samples_list.map(index => index.steps),
            y: samples_list.map(index => index.date),
            type: "bar"
        };

        let layout = {
            title: "Daily Steps"
        }
    
        // Data array
        let data = [trace]
    
        // Render the plot to the div tag with id "plot"
        Plotly.newPlot("bar", data, layout)
    }