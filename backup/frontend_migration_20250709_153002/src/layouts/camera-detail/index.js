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
import { useParams, useHistory } from "react-router-dom";

// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import Icon from "@mui/material/Icon";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiButton from "components/VuiButton";
import VuiProgress from "components/VuiProgress";

// Vision UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import MiniStatisticsCard from "examples/Cards/StatisticsCards/MiniStatisticsCard";

// Charts
import LineChart from "examples/Charts/LineCharts/LineChart";

// React icons
import { IoArrowBack } from "react-icons/io5";
import { IoCamera } from "react-icons/io5";
import { IoPlay } from "react-icons/io5";
import { IoStop } from "react-icons/io5";
import { IoPencil } from "react-icons/io5";
import { IoPeople } from "react-icons/io5";
import { IoTrendingUp } from "react-icons/io5";
import { IoTrendingDown } from "react-icons/io5";
import { IoAnalytics } from "react-icons/io5";

// Services
import { cameraAPI } from "services/cameraAPI";

// Camera status colors
const getStatusColor = (status) => {
  switch (status) {
    case 'active':
      return 'success';
    case 'offline':
      return 'error';
    case 'maintenance':
      return 'warning';
    case 'error':
      return 'error';
    default:
      return 'info';
  }
};

function CameraDetail() {
  const { id } = useParams();
  const history = useHistory();
  const [camera, setCamera] = useState(null);
  const [countData, setCountData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const [processingStatus, setProcessingStatus] = useState('stopped');

  // Load camera data on component mount
  useEffect(() => {
    loadCameraData();
  }, [id]);

  const loadCameraData = async () => {
    try {
      setLoading(true);
      
      // Load camera details
      const cameraData = await cameraAPI.getCameraById(id);
      setCamera(cameraData);
      
      // Load count data for this camera
      const counts = await cameraAPI.getCountData(id, 50);
      setCountData(counts);
      
      setError(null);
    } catch (err) {
      setError(err.message);
      setSnackbar({ open: true, message: err.message, severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (newStatus) => {
    try {
      await cameraAPI.updateCamera(id, { status: newStatus });
      setSnackbar({ open: true, message: 'Camera status updated!', severity: 'success' });
      loadCameraData();
    } catch (err) {
      setSnackbar({ open: true, message: err.message, severity: 'error' });
    }
  };

  const handleStartProcessing = async () => {
    try {
      await cameraAPI.makeRequest(`/cameras/${id}/start`, { method: 'POST' });
      setProcessingStatus('running');
      setSnackbar({ open: true, message: 'Camera processing started!', severity: 'success' });
    } catch (err) {
      setSnackbar({ open: true, message: err.message, severity: 'error' });
    }
  };

  const handleStopProcessing = async () => {
    try {
      await cameraAPI.makeRequest(`/cameras/${id}/stop`, { method: 'POST' });
      setProcessingStatus('stopped');
      setSnackbar({ open: true, message: 'Camera processing stopped!', severity: 'success' });
    } catch (err) {
      setSnackbar({ open: true, message: err.message, severity: 'error' });
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Prepare chart data
  const prepareChartData = () => {
    if (!countData.length) return null;

    const sortedData = countData.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
    const labels = sortedData.map(item => new Date(item.timestamp).toLocaleTimeString());
    const peopleIn = sortedData.map(item => item.people_in);
    const peopleOut = sortedData.map(item => item.people_out);
    const currentCount = sortedData.map(item => item.current_count);

    return {
      labels,
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
        {
          label: "Current Count",
          data: currentCount,
          color: "success",
          tension: 0.4,
        },
      ],
    };
  };

  const chartData = prepareChartData();

  // Chart options
  const chartOptions = {
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

  // Calculate statistics
  const totalIn = countData.reduce((sum, item) => sum + item.people_in, 0);
  const totalOut = countData.reduce((sum, item) => sum + item.people_out, 0);
  const averageConfidence = countData.length > 0 
    ? countData.reduce((sum, item) => sum + item.confidence, 0) / countData.length 
    : 0;
  const currentCount = countData.length > 0 ? countData[countData.length - 1]?.current_count : 0;

  if (loading) {
    return (
      <DashboardLayout>
        <DashboardNavbar />
        <VuiBox display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <VuiTypography color="text">Loading camera details...</VuiTypography>
        </VuiBox>
        <Footer />
      </DashboardLayout>
    );
  }

  if (!camera) {
    return (
      <DashboardLayout>
        <DashboardNavbar />
        <VuiBox display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <VuiTypography color="text">Camera not found</VuiTypography>
        </VuiBox>
        <Footer />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <VuiBox py={3}>
        {/* Header */}
        <VuiBox mb={3}>
          <VuiBox display="flex" alignItems="center" mb={2}>
            <VuiButton
              color="info"
              variant="text"
              startIcon={<IoArrowBack />}
              onClick={() => history.push('/cameras')}
              sx={{ mr: 2 }}
            >
              Back to Cameras
            </VuiButton>
            <VuiTypography variant="h3" color="white" fontWeight="bold">
              {camera.name}
            </VuiTypography>
          </VuiBox>
          
          <VuiBox display="flex" alignItems="center" gap={2}>
            <Chip
              label={camera.status}
              color={getStatusColor(camera.status)}
              size="medium"
            />
            <VuiTypography variant="button" color="text">
              {camera.location}
            </VuiTypography>
          </VuiBox>
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
                title={{ text: "Total People In", fontWeight: "regular" }}
                count={totalIn.toString()}
                percentage={{ color: "success", text: "All Time" }}
                icon={{ color: "info", component: <IoTrendingUp size="22px" color="white" /> }}
              />
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Total People Out" }}
                count={totalOut.toString()}
                percentage={{ color: "error", text: "All Time" }}
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
                title={{ text: "Accuracy" }}
                count={`${(averageConfidence * 100).toFixed(1)}%`}
                percentage={{ color: "info", text: "Average" }}
                icon={{ color: "info", component: <IoAnalytics size="22px" color="white" /> }}
              />
            </Grid>
          </Grid>
        </VuiBox>

        {/* Camera Controls */}
        <VuiBox mb={3}>
          <Card>
            <VuiBox p={3}>
              <VuiTypography variant="h6" color="white" fontWeight="bold" mb={3}>
                Camera Controls
              </VuiTypography>
              
              <Grid container spacing={3} alignItems="center">
                <Grid item xs={12} md={4}>
                  <VuiBox>
                    <VuiTypography variant="button" color="text" fontWeight="medium" mb={2}>
                      Processing Status
                    </VuiTypography>
                    <VuiBox display="flex" gap={2}>
                      <VuiButton
                        color="success"
                        variant={processingStatus === 'running' ? 'contained' : 'outlined'}
                        startIcon={<IoPlay />}
                        onClick={handleStartProcessing}
                        disabled={processingStatus === 'running'}
                      >
                        Start
                      </VuiButton>
                      <VuiButton
                        color="error"
                        variant={processingStatus === 'stopped' ? 'contained' : 'outlined'}
                        startIcon={<IoStop />}
                        onClick={handleStopProcessing}
                        disabled={processingStatus === 'stopped'}
                      >
                        Stop
                      </VuiButton>
                    </VuiBox>
                  </VuiBox>
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <VuiBox>
                    <VuiTypography variant="button" color="text" fontWeight="medium" mb={2}>
                      Camera Status
                    </VuiTypography>
                    <FormControl fullWidth size="small">
                      <InputLabel>Status</InputLabel>
                      <Select
                        value={camera.status}
                        label="Status"
                        onChange={(e) => handleStatusChange(e.target.value)}
                      >
                        <MenuItem value="active">Active</MenuItem>
                        <MenuItem value="offline">Offline</MenuItem>
                        <MenuItem value="maintenance">Maintenance</MenuItem>
                        <MenuItem value="error">Error</MenuItem>
                      </Select>
                    </FormControl>
                  </VuiBox>
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <VuiBox>
                    <VuiTypography variant="button" color="text" fontWeight="medium" mb={2}>
                      Stream URL
                    </VuiTypography>
                    <VuiTypography variant="caption" color="text" sx={{ wordBreak: 'break-all' }}>
                      {camera.stream_url || 'No stream URL configured'}
                    </VuiTypography>
                  </VuiBox>
                </Grid>
              </Grid>
            </VuiBox>
          </Card>
        </VuiBox>

        {/* Chart Section */}
        <VuiBox mb={3}>
          <Card>
            <VuiBox p={3}>
              <VuiTypography variant="h6" color="white" fontWeight="bold" mb={3}>
                People Count Over Time
              </VuiTypography>
              
              <VuiBox sx={{ height: "400px" }}>
                {chartData ? (
                  <LineChart lineChartData={chartData} lineChartOptions={chartOptions} />
                ) : (
                  <VuiBox display="flex" justifyContent="center" alignItems="center" height="100%">
                    <VuiTypography color="text">No count data available</VuiTypography>
                  </VuiBox>
                )}
              </VuiBox>
            </VuiBox>
          </Card>
        </VuiBox>

        {/* Recent Count Data */}
        <VuiBox mb={3}>
          <Card>
            <VuiBox p={3}>
              <VuiTypography variant="h6" color="white" fontWeight="bold" mb={3}>
                Recent Count Data
              </VuiTypography>
              
              {countData.length === 0 ? (
                <VuiBox display="flex" justifyContent="center" py={4}>
                  <VuiTypography color="text">No count data available</VuiTypography>
                </VuiBox>
              ) : (
                <Grid container spacing={2}>
                  {countData.slice(0, 12).map((item, index) => (
                    <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
                      <VuiBox
                        p={2}
                        borderRadius="lg"
                        sx={{
                          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        }}
                      >
                        <VuiBox display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                          <VuiTypography variant="caption" color="white" fontWeight="bold">
                            Record #{index + 1}
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
                  ))}
                </Grid>
              )}
            </VuiBox>
          </Card>
        </VuiBox>

        {/* Camera Information */}
        <VuiBox mb={3}>
          <Card>
            <VuiBox p={3}>
              <VuiTypography variant="h6" color="white" fontWeight="bold" mb={3}>
                Camera Information
              </VuiTypography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <VuiBox>
                    <VuiTypography variant="button" color="text" fontWeight="medium" mb={2}>
                      Basic Details
                    </VuiTypography>
                    
                    <VuiBox mb={2}>
                      <VuiTypography variant="caption" color="text">Camera ID</VuiTypography>
                      <VuiTypography variant="button" color="white" fontWeight="bold">
                        {camera.id}
                      </VuiTypography>
                    </VuiBox>
                    
                    <VuiBox mb={2}>
                      <VuiTypography variant="caption" color="text">Name</VuiTypography>
                      <VuiTypography variant="button" color="white" fontWeight="bold">
                        {camera.name}
                      </VuiTypography>
                    </VuiBox>
                    
                    <VuiBox mb={2}>
                      <VuiTypography variant="caption" color="text">Location</VuiTypography>
                      <VuiTypography variant="button" color="white" fontWeight="bold">
                        {camera.location}
                      </VuiTypography>
                    </VuiBox>
                  </VuiBox>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <VuiBox>
                    <VuiTypography variant="button" color="text" fontWeight="medium" mb={2}>
                      System Information
                    </VuiTypography>
                    
                    <VuiBox mb={2}>
                      <VuiTypography variant="caption" color="text">Created Date</VuiTypography>
                      <VuiTypography variant="button" color="white" fontWeight="bold">
                        {new Date(camera.created_at).toLocaleDateString()}
                      </VuiTypography>
                    </VuiBox>
                    
                    <VuiBox mb={2}>
                      <VuiTypography variant="caption" color="text">Total Records</VuiTypography>
                      <VuiTypography variant="button" color="white" fontWeight="bold">
                        {countData.length}
                      </VuiTypography>
                    </VuiBox>
                    
                    <VuiBox mb={2}>
                      <VuiTypography variant="caption" color="text">Last Updated</VuiTypography>
                      <VuiTypography variant="button" color="white" fontWeight="bold">
                        {countData.length > 0 
                          ? new Date(countData[countData.length - 1].timestamp).toLocaleString()
                          : 'Never'
                        }
                      </VuiTypography>
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

export default CameraDetail; 