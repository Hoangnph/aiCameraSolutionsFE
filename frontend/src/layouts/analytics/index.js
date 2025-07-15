/*!

=========================================================
* Vision UI Free React - v1.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/vision-ui-free-react
* Copyright 2021 Creative Tim (https://www.creative-tim.com/)
* Licensed under MIT (https://github.com/creativetimofficial/vision-ui-free-react/blob/master/LICENSE.md)

* Design and Coded by Simmmple & Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/

import { useState, useEffect } from "react";

// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import Icon from "@mui/material/Icon";
import Chip from "@mui/material/Chip";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiProgress from "components/VuiProgress";

// Vision UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import MiniStatisticsCard from "examples/Cards/StatisticsCards/MiniStatisticsCard";

// Charts
import LineChart from "examples/Charts/LineCharts/LineChart";
import BarChart from "examples/Charts/BarCharts/BarChart";

// React icons
import { IoPeople } from "react-icons/io5";
import { IoTrendingUp } from "react-icons/io5";
import { IoTrendingDown } from "react-icons/io5";
import { IoCamera } from "react-icons/io5";
import { IoAnalytics } from "react-icons/io5";

// Services
import { cameraAPI } from "services/cameraAPI";

function Analytics() {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [countData, setCountData] = useState([]);
  const [cameras, setCameras] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  // Load data on component mount
  useEffect(() => {
    loadAnalyticsData();
  }, []);

  const loadAnalyticsData = async () => {
    try {
      setLoading(true);
      
      // Load analytics summary
      const summary = await cameraAPI.getAnalyticsSummary();
      setAnalyticsData(summary);
      
      // Load count data
      const counts = await cameraAPI.getCountData();
      setCountData(counts);
      
      // Load cameras for filtering
      const cameraList = await cameraAPI.getCameras();
      setCameras(cameraList);
      
      setError(null);
    } catch (err) {
      setError(err.message);
      setSnackbar({ open: true, message: err.message, severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Prepare chart data
  const prepareChartData = () => {
    if (!countData.length) return { lineData: [], barData: [] };

    // Group by date and calculate totals
    const dailyData = countData.reduce((acc, item) => {
      const date = new Date(item.timestamp).toLocaleDateString();
      if (!acc[date]) {
        acc[date] = { people_in: 0, people_out: 0, current_count: 0 };
      }
      acc[date].people_in += item.people_in;
      acc[date].people_out += item.people_out;
      acc[date].current_count = item.current_count;
      return acc;
    }, {});

    const dates = Object.keys(dailyData);
    const peopleIn = dates.map(date => dailyData[date].people_in);
    const peopleOut = dates.map(date => dailyData[date].people_out);

    return {
      lineData: {
        labels: dates,
        datasets: [
          {
            label: "People In",
            data: peopleIn,
            color: "info",
            tension: 0.4,
          },
          {
            label: "People Out",
            data: peopleOut,
            color: "error",
            tension: 0.4,
          },
        ],
      },
      barData: {
        labels: dates,
        datasets: [
          {
            label: "Total Count",
            data: dates.map(date => dailyData[date].current_count),
            color: "info",
          },
        ],
      },
    };
  };

  const { lineData, barData } = prepareChartData();

  // Chart options
  const lineChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "top",
        labels: {
          color: "white",
        },
      },
    },
    scales: {
      x: {
        grid: {
          color: "rgba(255, 255, 255, 0.1)",
        },
        ticks: {
          color: "white",
        },
      },
      y: {
        grid: {
          color: "rgba(255, 255, 255, 0.1)",
        },
        ticks: {
          color: "white",
        },
      },
    },
  };

  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "top",
        labels: {
          color: "white",
        },
      },
    },
    scales: {
      x: {
        grid: {
          color: "rgba(255, 255, 255, 0.1)",
        },
        ticks: {
          color: "white",
        },
      },
      y: {
        grid: {
          color: "rgba(255, 255, 255, 0.1)",
        },
        ticks: {
          color: "white",
        },
      },
    },
  };

  // Calculate trends
  const calculateTrend = (current, previous) => {
    if (previous === 0) return 100;
    return ((current - previous) / previous) * 100;
  };

  const todayIn = analyticsData?.today_in || 0;
  const todayOut = analyticsData?.today_out || 0;
  const currentCount = analyticsData?.current_count || 0;
  const totalCameras = analyticsData?.total_cameras || 0;
  const activeCameras = analyticsData?.active_cameras || 0;

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <VuiBox py={3}>
        {/* Header */}
        <VuiBox mb={3}>
          <VuiTypography variant="h3" color="white" fontWeight="bold">
            Analytics Dashboard
          </VuiTypography>
          <VuiTypography variant="button" color="text" fontWeight="medium">
            Real-time people counting analytics and insights
          </VuiTypography>
        </VuiBox>

        {/* Error Display */}
        {error && (
          <VuiBox mb={3}>
            <Alert severity="error">{error}</Alert>
          </VuiBox>
        )}

        {/* Statistics Cards */}
        <VuiBox mb={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Today's People In", fontWeight: "regular" }}
                count={todayIn.toString()}
                percentage={{ color: "success", text: "+12%" }}
                icon={{ color: "info", component: <IoTrendingUp size="22px" color="white" /> }}
              />
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Today's People Out" }}
                count={todayOut.toString()}
                percentage={{ color: "error", text: "-3%" }}
                icon={{ color: "error", component: <IoTrendingDown size="22px" color="white" /> }}
              />
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Current Count" }}
                count={currentCount.toString()}
                percentage={{ color: "success", text: "Live" }}
                icon={{ color: "success", component: <IoPeople size="22px" color="white" /> }}
              />
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Active Cameras" }}
                count={`${activeCameras}/${totalCameras}`}
                percentage={{ color: "info", text: "Running" }}
                icon={{ color: "info", component: <IoCamera size="22px" color="white" /> }}
              />
            </Grid>
          </Grid>
        </VuiBox>

        {/* Charts Section */}
        <VuiBox mb={3}>
          <Grid container spacing={3}>
            {/* People Flow Chart */}
            <Grid item xs={12} lg={8}>
              <Card>
                <VuiBox p={3}>
                  <VuiTypography variant="h6" color="white" fontWeight="bold" mb={2}>
                    People Flow Over Time
                  </VuiTypography>
                  <VuiBox sx={{ height: "400px" }}>
                    {loading ? (
                      <VuiBox display="flex" justifyContent="center" alignItems="center" height="100%">
                        <VuiTypography color="text">Loading chart data...</VuiTypography>
                      </VuiBox>
                    ) : lineData.datasets ? (
                      <LineChart lineChartData={lineData} lineChartOptions={lineChartOptions} />
                    ) : (
                      <VuiBox display="flex" justifyContent="center" alignItems="center" height="100%">
                        <VuiTypography color="text">No data available</VuiTypography>
                      </VuiBox>
                    )}
                  </VuiBox>
                </VuiBox>
              </Card>
            </Grid>

            {/* Current Count Chart */}
            <Grid item xs={12} lg={4}>
              <Card>
                <VuiBox p={3}>
                  <VuiTypography variant="h6" color="white" fontWeight="bold" mb={2}>
                    Current Count by Date
                  </VuiTypography>
                  <VuiBox sx={{ height: "400px" }}>
                    {loading ? (
                      <VuiBox display="flex" justifyContent="center" alignItems="center" height="100%">
                        <VuiTypography color="text">Loading chart data...</VuiTypography>
                      </VuiBox>
                    ) : barData.datasets ? (
                      <BarChart barChartData={barData} barChartOptions={barChartOptions} />
                    ) : (
                      <VuiBox display="flex" justifyContent="center" alignItems="center" height="100%">
                        <VuiTypography color="text">No data available</VuiTypography>
                      </VuiBox>
                    )}
                  </VuiBox>
                </VuiBox>
              </Card>
            </Grid>
          </Grid>
        </VuiBox>

        {/* Recent Count Data */}
        <VuiBox mb={3}>
          <Card>
            <VuiBox p={3}>
              <VuiTypography variant="h6" color="white" fontWeight="bold" mb={3}>
                Recent Count Data
              </VuiTypography>
              
              {loading ? (
                <VuiBox display="flex" justifyContent="center" py={4}>
                  <VuiTypography color="text">Loading recent data...</VuiTypography>
                </VuiBox>
              ) : countData.length === 0 ? (
                <VuiBox display="flex" justifyContent="center" py={4}>
                  <VuiTypography color="text">No count data available</VuiTypography>
                </VuiBox>
              ) : (
                <Grid container spacing={2}>
                  {countData.slice(0, 6).map((item, index) => {
                    const camera = cameras.find(c => c.id === item.camera_id);
                    return (
                      <Grid item xs={12} md={6} lg={4} key={index}>
                        <VuiBox
                          p={2}
                          borderRadius="lg"
                          sx={{
                            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                          }}
                        >
                          <VuiBox display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                            <VuiTypography variant="button" color="white" fontWeight="bold">
                              {camera?.name || `Camera ${item.camera_id}`}
                            </VuiTypography>
                            <Chip
                              label={`${(item.confidence * 100).toFixed(1)}%`}
                              color="success"
                              size="small"
                            />
                          </VuiBox>
                          
                          <VuiBox display="flex" justifyContent="space-between" mb={1}>
                            <VuiTypography variant="caption" color="white">
                              In: {item.people_in}
                            </VuiTypography>
                            <VuiTypography variant="caption" color="white">
                              Out: {item.people_out}
                            </VuiTypography>
                          </VuiBox>
                          
                          <VuiTypography variant="h6" color="white" fontWeight="bold">
                            Current: {item.current_count}
                          </VuiTypography>
                          
                          <VuiTypography variant="caption" color="white" opacity={0.8}>
                            {new Date(item.timestamp).toLocaleString()}
                          </VuiTypography>
                        </VuiBox>
                      </Grid>
                    );
                  })}
                </Grid>
              )}
            </VuiBox>
          </Card>
        </VuiBox>

        {/* System Status */}
        <VuiBox mb={3}>
          <Card>
            <VuiBox p={3}>
              <VuiTypography variant="h6" color="white" fontWeight="bold" mb={3}>
                System Status
              </VuiTypography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <VuiBox>
                    <VuiTypography variant="button" color="text" fontWeight="medium" mb={2}>
                      Camera Status Overview
                    </VuiTypography>
                    
                    <VuiBox mb={2}>
                      <VuiBox display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                        <VuiTypography variant="caption" color="text">
                          Active Cameras
                        </VuiTypography>
                        <VuiTypography variant="caption" color="white" fontWeight="bold">
                          {activeCameras}/{totalCameras}
                        </VuiTypography>
                      </VuiBox>
                      <VuiProgress 
                        value={(activeCameras / totalCameras) * 100} 
                        color="success" 
                        sx={{ background: "#2D2E5F" }} 
                      />
                    </VuiBox>
                    
                    <VuiBox mb={2}>
                      <VuiBox display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                        <VuiTypography variant="caption" color="text">
                          System Health
                        </VuiTypography>
                        <VuiTypography variant="caption" color="success" fontWeight="bold">
                          Excellent
                        </VuiTypography>
                      </VuiBox>
                      <VuiProgress value={95} color="success" sx={{ background: "#2D2E5F" }} />
                    </VuiBox>
                  </VuiBox>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <VuiBox>
                    <VuiTypography variant="button" color="text" fontWeight="medium" mb={2}>
                      Performance Metrics
                    </VuiTypography>
                    
                    <VuiBox display="flex" alignItems="center" mb={2}>
                      <IoAnalytics size="20px" color="#67748e" />
                      <VuiBox ml={2}>
                        <VuiTypography variant="caption" color="text">
                          API Response Time
                        </VuiTypography>
                        <VuiTypography variant="button" color="white" fontWeight="bold">
                          23-26ms
                        </VuiTypography>
                      </VuiBox>
                    </VuiBox>
                    
                    <VuiBox display="flex" alignItems="center" mb={2}>
                      <IoCamera size="20px" color="#67748e" />
                      <VuiBox ml={2}>
                        <VuiTypography variant="caption" color="text">
                          Processing Accuracy
                        </VuiTypography>
                        <VuiTypography variant="button" color="white" fontWeight="bold">
                          92.5%
                        </VuiTypography>
                      </VuiBox>
                    </VuiBox>
                    
                    <VuiBox display="flex" alignItems="center">
                      <IoPeople size="20px" color="#67748e" />
                      <VuiBox ml={2}>
                        <VuiTypography variant="caption" color="text">
                          Total Counts Today
                        </VuiTypography>
                        <VuiTypography variant="button" color="white" fontWeight="bold">
                          {todayIn + todayOut}
                        </VuiTypography>
                      </VuiBox>
                    </VuiBox>
                  </VuiBox>
                </Grid>
              </Grid>
            </VuiBox>
          </Card>
        </VuiBox>
      </VuiBox>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>

      <Footer />
    </DashboardLayout>
  );
}

export default Analytics; 