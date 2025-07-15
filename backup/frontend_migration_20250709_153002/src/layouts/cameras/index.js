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
import { useHistory } from "react-router-dom";

// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import Icon from "@mui/material/Icon";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import TextField from "@mui/material/TextField";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import Chip from "@mui/material/Chip";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiButton from "components/VuiButton";

// Vision UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import MiniStatisticsCard from "examples/Cards/StatisticsCards/MiniStatisticsCard";

// React icons
import { IoCamera } from "react-icons/io5";
import { IoAdd } from "react-icons/io5";
import { IoEye } from "react-icons/io5";
import { IoPencil } from "react-icons/io5";
import { IoTrash } from "react-icons/io5";
import { IoPlay } from "react-icons/io5";
import { IoStop } from "react-icons/io5";

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

function Cameras() {
  const history = useHistory();
  const [cameras, setCameras] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openAddDialog, setOpenAddDialog] = useState(false);
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  // Form states
  const [formData, setFormData] = useState({
    name: '',
    location: '',
    stream_url: '',
    status: 'offline'
  });

  // Load cameras on component mount
  useEffect(() => {
    loadCameras();
  }, []);

  const loadCameras = async () => {
    try {
      setLoading(true);
      const data = await cameraAPI.getCameras();
      setCameras(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      setSnackbar({ open: true, message: err.message, severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleAddCamera = async () => {
    try {
      await cameraAPI.createCamera(formData);
      setSnackbar({ open: true, message: 'Camera added successfully!', severity: 'success' });
      setOpenAddDialog(false);
      resetForm();
      loadCameras();
    } catch (err) {
      setSnackbar({ open: true, message: err.message, severity: 'error' });
    }
  };

  const handleEditCamera = async () => {
    try {
      await cameraAPI.updateCamera(selectedCamera.id, formData);
      setSnackbar({ open: true, message: 'Camera updated successfully!', severity: 'success' });
      setOpenEditDialog(false);
      resetForm();
      loadCameras();
    } catch (err) {
      setSnackbar({ open: true, message: err.message, severity: 'error' });
    }
  };

  const handleDeleteCamera = async () => {
    try {
      await cameraAPI.deleteCamera(selectedCamera.id);
      setSnackbar({ open: true, message: 'Camera deleted successfully!', severity: 'success' });
      setOpenDeleteDialog(false);
      loadCameras();
    } catch (err) {
      setSnackbar({ open: true, message: err.message, severity: 'error' });
    }
  };

  const handleStatusChange = async (cameraId, newStatus) => {
    try {
      await cameraAPI.updateCamera(cameraId, { status: newStatus });
      setSnackbar({ open: true, message: 'Camera status updated!', severity: 'success' });
      loadCameras();
    } catch (err) {
      setSnackbar({ open: true, message: err.message, severity: 'error' });
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      location: '',
      stream_url: '',
      status: 'offline'
    });
  };

  const openEditModal = (camera) => {
    setSelectedCamera(camera);
    setFormData({
      name: camera.name,
      location: camera.location,
      stream_url: camera.stream_url,
      status: camera.status
    });
    setOpenEditDialog(true);
  };

  const openDeleteModal = (camera) => {
    setSelectedCamera(camera);
    setOpenDeleteDialog(true);
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Statistics
  const totalCameras = cameras.length;
  const activeCameras = cameras.filter(c => c.status === 'active').length;
  const offlineCameras = cameras.filter(c => c.status === 'offline').length;
  const maintenanceCameras = cameras.filter(c => c.status === 'maintenance').length;

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <VuiBox py={3}>
        {/* Statistics Cards */}
        <VuiBox mb={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Total Cameras", fontWeight: "regular" }}
                count={totalCameras.toString()}
                percentage={{ color: "info", text: "All Systems" }}
                icon={{ color: "info", component: <IoCamera size="22px" color="white" /> }}
              />
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Active Cameras" }}
                count={activeCameras.toString()}
                percentage={{ color: "success", text: "Running" }}
                icon={{ color: "success", component: <IoPlay size="22px" color="white" /> }}
              />
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Offline Cameras" }}
                count={offlineCameras.toString()}
                percentage={{ color: "error", text: "Stopped" }}
                icon={{ color: "error", component: <IoStop size="22px" color="white" /> }}
              />
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Maintenance" }}
                count={maintenanceCameras.toString()}
                percentage={{ color: "warning", text: "In Progress" }}
                icon={{ color: "warning", component: <IoPencil size="22px" color="white" /> }}
              />
            </Grid>
          </Grid>
        </VuiBox>

        {/* Header with Add Button */}
        <VuiBox mb={3} display="flex" justifyContent="space-between" alignItems="center">
          <VuiTypography variant="h3" color="white" fontWeight="bold">
            Camera Management
          </VuiTypography>
          <VuiButton
            color="info"
            variant="contained"
            startIcon={<IoAdd />}
            onClick={() => setOpenAddDialog(true)}
          >
            Add Camera
          </VuiButton>
        </VuiBox>

        {/* Error Display */}
        {error && (
          <VuiBox mb={3}>
            <Alert severity="error">{error}</Alert>
          </VuiBox>
        )}

        {/* Cameras Grid */}
        <Grid container spacing={3}>
          {loading ? (
            <Grid item xs={12}>
              <VuiBox display="flex" justifyContent="center" py={4}>
                <VuiTypography color="text">Loading cameras...</VuiTypography>
              </VuiBox>
            </Grid>
          ) : cameras.length === 0 ? (
            <Grid item xs={12}>
              <Card>
                <VuiBox display="flex" justifyContent="center" alignItems="center" py={8}>
                  <VuiBox textAlign="center">
                    <IoCamera size="48px" color="#67748e" />
                    <VuiTypography variant="h6" color="text" mt={2}>
                      No cameras found
                    </VuiTypography>
                    <VuiTypography variant="button" color="text" mt={1}>
                      Add your first camera to get started
                    </VuiTypography>
                  </VuiBox>
                </VuiBox>
              </Card>
            </Grid>
          ) : (
            cameras.map((camera) => (
              <Grid item xs={12} md={6} lg={4} key={camera.id}>
                <Card>
                  <VuiBox p={3}>
                    {/* Camera Header */}
                    <VuiBox display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                      <VuiTypography variant="h6" color="white" fontWeight="bold">
                        {camera.name}
                      </VuiTypography>
                      <Chip
                        label={camera.status}
                        color={getStatusColor(camera.status)}
                        size="small"
                      />
                    </VuiBox>

                    {/* Camera Details */}
                    <VuiBox mb={3}>
                      <VuiTypography variant="button" color="text" fontWeight="medium">
                        Location: {camera.location}
                      </VuiTypography>
                      <VuiTypography variant="button" color="text" fontWeight="medium" display="block" mt={1}>
                        Created: {new Date(camera.created_at).toLocaleDateString()}
                      </VuiTypography>
                    </VuiBox>

                    {/* Action Buttons */}
                    <VuiBox display="flex" gap={1} flexWrap="wrap">
                      <VuiButton
                        color="info"
                        variant="outlined"
                        size="small"
                        startIcon={<IoEye />}
                        onClick={() => history.push(`/cameras/${camera.id}`)}
                      >
                        View
                      </VuiButton>
                      <VuiButton
                        color="warning"
                        variant="outlined"
                        size="small"
                        startIcon={<IoPencil />}
                        onClick={() => openEditModal(camera)}
                      >
                        Edit
                      </VuiButton>
                      <VuiButton
                        color="error"
                        variant="outlined"
                        size="small"
                        startIcon={<IoTrash />}
                        onClick={() => openDeleteModal(camera)}
                      >
                        Delete
                      </VuiButton>
                    </VuiBox>

                    {/* Status Control */}
                    <VuiBox mt={2}>
                      <FormControl fullWidth size="small">
                        <InputLabel>Status</InputLabel>
                        <Select
                          value={camera.status}
                          label="Status"
                          onChange={(e) => handleStatusChange(camera.id, e.target.value)}
                        >
                          <MenuItem value="active">Active</MenuItem>
                          <MenuItem value="offline">Offline</MenuItem>
                          <MenuItem value="maintenance">Maintenance</MenuItem>
                          <MenuItem value="error">Error</MenuItem>
                        </Select>
                      </FormControl>
                    </VuiBox>
                  </VuiBox>
                </Card>
              </Grid>
            ))
          )}
        </Grid>
      </VuiBox>

      {/* Add Camera Dialog */}
      <Dialog open={openAddDialog} onClose={() => setOpenAddDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add New Camera</DialogTitle>
        <DialogContent>
          <VuiBox pt={2}>
            <TextField
              fullWidth
              label="Camera Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Location"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Stream URL"
              value={formData.stream_url}
              onChange={(e) => setFormData({ ...formData, stream_url: e.target.value })}
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>Status</InputLabel>
              <Select
                value={formData.status}
                label="Status"
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              >
                <MenuItem value="active">Active</MenuItem>
                <MenuItem value="offline">Offline</MenuItem>
                <MenuItem value="maintenance">Maintenance</MenuItem>
                <MenuItem value="error">Error</MenuItem>
              </Select>
            </FormControl>
          </VuiBox>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAddDialog(false)}>Cancel</Button>
          <Button onClick={handleAddCamera} variant="contained" color="primary">
            Add Camera
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Camera Dialog */}
      <Dialog open={openEditDialog} onClose={() => setOpenEditDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Camera</DialogTitle>
        <DialogContent>
          <VuiBox pt={2}>
            <TextField
              fullWidth
              label="Camera Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Location"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Stream URL"
              value={formData.stream_url}
              onChange={(e) => setFormData({ ...formData, stream_url: e.target.value })}
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>Status</InputLabel>
              <Select
                value={formData.status}
                label="Status"
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              >
                <MenuItem value="active">Active</MenuItem>
                <MenuItem value="offline">Offline</MenuItem>
                <MenuItem value="maintenance">Maintenance</MenuItem>
                <MenuItem value="error">Error</MenuItem>
              </Select>
            </FormControl>
          </VuiBox>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEditDialog(false)}>Cancel</Button>
          <Button onClick={handleEditCamera} variant="contained" color="primary">
            Update Camera
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Camera Dialog */}
      <Dialog open={openDeleteDialog} onClose={() => setOpenDeleteDialog(false)}>
        <DialogTitle>Delete Camera</DialogTitle>
        <DialogContent>
          <VuiTypography>
            Are you sure you want to delete "{selectedCamera?.name}"? This action cannot be undone.
          </VuiTypography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDeleteDialog(false)}>Cancel</Button>
          <Button onClick={handleDeleteCamera} variant="contained" color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

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

export default Cameras; 