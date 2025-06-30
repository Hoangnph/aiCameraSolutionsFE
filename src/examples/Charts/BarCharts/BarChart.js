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

import React, { Component } from "react";
import Chart from "react-apexcharts";

class BarChart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      chartData: [],
      chartOptions: {},
    };
  }

  componentDidMount() {
    const { barChartData, barChartOptions } = this.props;
    console.log('BarChart data:', barChartData, barChartOptions);
    this.setState({
      chartData: barChartData,
      chartOptions: barChartOptions,
    });
  }

  componentDidUpdate(prevProps) {
    if (
      prevProps.barChartData !== this.props.barChartData ||
      prevProps.barChartOptions !== this.props.barChartOptions
    ) {
      console.log('BarChart data updated:', this.props.barChartData, this.props.barChartOptions);
      this.setState({
        chartData: this.props.barChartData,
        chartOptions: this.props.barChartOptions,
      });
    }
  }

  render() {
    return (
      <Chart
        options={this.state.chartOptions}
        series={this.state.chartData}
        type="bar"
        width="100%"
        height="100%"
      />
    );
  }
}

export default BarChart;
