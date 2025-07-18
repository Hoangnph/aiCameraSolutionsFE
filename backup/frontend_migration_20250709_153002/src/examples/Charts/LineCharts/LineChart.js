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
    this.setState({
      chartData: lineChartData,
      chartOptions: lineChartOptions,
    });
  }

  componentDidUpdate(prevProps) {
    if (
      prevProps.lineChartData !== this.props.lineChartData ||
      prevProps.lineChartOptions !== this.props.lineChartOptions
    ) {
      console.log('LineChart data updated:', this.props.lineChartData, this.props.lineChartOptions);
      this.setState({
        chartData: this.props.lineChartData,
        chartOptions: this.props.lineChartOptions,
      });
    }
  }

  render() {
    return (
      <ReactApexChart
        options={this.state.chartOptions}
        series={this.state.chartData}
        type="area"
        width="100%"
        height="100%"
      />
    );
  }
}

export default LineChart;
