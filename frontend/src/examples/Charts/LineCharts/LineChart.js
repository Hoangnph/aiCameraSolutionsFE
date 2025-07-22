/*!

=========================================================
* Vision UI Free React - v1.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/vision-ui-free-react
* Copyright 2021 Creative Tim (https://www.creative-tim.com/)
* Licensed under MIT (https://github.com/creativetimofficial/vision-ui-free-react/blob/master LICENSE.md)

* Design and Coded by Simmmple & Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/

import React from "react";
import ReactApexChart from "react-apexcharts";

class LineChart extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      chartData: [],
      chartOptions: {},
    };
  }

  componentDidMount() {
    const { lineChartData, lineChartOptions } = this.props;
    console.log('LineChart data:', lineChartData, lineChartOptions);
    
    // Validate data before setting state
    const validData = Array.isArray(lineChartData) ? lineChartData : [];
    const validOptions = lineChartOptions || {};
    
    this.setState({
      chartData: validData,
      chartOptions: validOptions,
    });
  }

  componentDidUpdate(prevProps) {
    if (
      prevProps.lineChartData !== this.props.lineChartData ||
      prevProps.lineChartOptions !== this.props.lineChartOptions
    ) {
      console.log('LineChart data updated:', this.props.lineChartData, this.props.lineChartOptions);
      
      // Validate data before setting state
      const validData = Array.isArray(this.props.lineChartData) ? this.props.lineChartData : [];
      const validOptions = this.props.lineChartOptions || {};
      
      this.setState({
        chartData: validData,
        chartOptions: validOptions,
      });
    }
  }

  render() {
    const { chartData, chartOptions } = this.state;
    
    // Additional validation before rendering
    if (!Array.isArray(chartData) || chartData.length === 0) {
      console.warn('LineChart: Invalid or empty chart data');
      return <div>No chart data available</div>;
    }
    
    return (
      <ReactApexChart
        options={chartOptions}
        series={chartData}
        type="area"
        width="100%"
        height="100%"
      />
    );
  }
}

export default LineChart;
