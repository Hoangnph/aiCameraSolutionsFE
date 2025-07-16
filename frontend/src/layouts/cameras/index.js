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
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiButton from "components/VuiButton";
import VuiInput from "components/VuiInput";
import CameraTable from "components/CameraTable";

// Vision UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import MiniStatisticsCard from "examples/Cards/StatisticsCards/MiniStatisticsCard";
import GradientBorder from "examples/GradientBorder";

// Vision UI Dashboard assets
import radialGradient from "assets/theme/functions/radialGradient";
import palette from "assets/theme/base/colors";
import borders from "assets/theme/base/borders";

// React icons
import { IoCamera } from "react-icons/io5";
import { IoAdd } from "react-icons/io5";
import { IoPlay } from "react-icons/io5";
import { IoStop } from "react-icons/io5";
import { IoPencil } from "react-icons/io5";
import { IoTrash } from "react-icons/io5";
import { IoClose } from "react-icons/io5";

// Services
import { cameraAPI } from "services/cameraAPI";

// Camera status colors and icons
const getStatusConfig = (status) => {
  switch (status) {
    case 'active':
      return { color: 'success', icon: <IoPlay size="16px" />, bgColor: 'success' };
    case 'offline':
      return { color: 'error', icon: <IoStop size="16px" />, bgColor: 'error' };
    case 'maintenance':
      return { color: 'warning', icon: <IoPencil size="16px" />, bgColor: 'warning' };
    case 'error':
      return { color: 'error', icon: <IoStop size="16px" />, bgColor: 'error' };
    default:
      return { color: 'info', icon: <IoCamera size="16px" />, bgColor: 'info' };
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
    ip_address: '',
    rtsp_url: '',
    status: 'offline'
  });

  const [editFormData, setEditFormData] = useState({
    name: '',
    ip_address: '',
    rtsp_url: '',
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
      ip_address: '',
      rtsp_url: '',
      status: 'offline'
    });
  };

  const openEditModal = (camera) => {
    setSelectedCamera(camera);
    setFormData({
      name: camera.name,
      ip_address: camera.ip_address,
      rtsp_url: camera.rtsp_url,
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

        {/* Cameras Table */}
        <CameraTable 
          cameras={cameras}
          loading={loading}
          onStatusChange={handleStatusChange}
          onEdit={openEditModal}
          onDelete={openDeleteModal}
        />
      </VuiBox>

      {/* Add Camera Dialog */}
      <Dialog 
        open={openAddDialog} 
        onClose={() => setOpenAddDialog(false)} 
        maxWidth="sm" 
        fullWidth
        PaperProps={{
          sx: {
            backgroundColor: '#1a2035',
            color: 'white',
            borderRadius: '16px'
          }
        }}
      >
        <DialogTitle sx={{ 
          borderBottom: '1px solid rgba(255,255,255,0.1)',
          pb: 2
        }}>
          <VuiBox display="flex" alignItems="center">
            <VuiBox
              bgColor="info"
              color="white"
              width="2.5rem"
              height="2.5rem"
              borderRadius="lg"
              display="flex"
              justifyContent="center"
              alignItems="center"
              mr={2}
            >
              <IoAdd size="20px" />
            </VuiBox>
            <VuiTypography variant="h6" color="white" fontWeight="bold">
              Add New Camera
            </VuiTypography>
          </VuiBox>
        </DialogTitle>
        <DialogContent sx={{ pt: 3 }}>
          <VuiBox>
            <VuiBox mb={3}>
              <VuiTypography variant="caption" color="text" opacity={0.7} display="block" mb={1}>
                Camera Name
              </VuiTypography>
              <TextField
                fullWidth
                placeholder="Enter camera name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    color: 'white',
                    '& fieldset': {
                      borderColor: 'rgba(255,255,255,0.2)'
                    },
                    '&:hover fieldset': {
                      borderColor: 'rgba(255,255,255,0.3)'
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#0075FF'
                    }
                  },
                  '& .MuiInputLabel-root': {
                    color: 'rgba(255,255,255,0.7)'
                  }
                }}
              />
            </VuiBox>
            
            <VuiBox mb={3}>
              <VuiTypography variant="caption" color="text" opacity={0.7} display="block" mb={1}>
                IP Address
              </VuiTypography>
              <VuiInput
                placeholder="192.168.1.100"
                value={formData.ip_address}
                onChange={(e) => setFormData({ ...formData, ip_address: e.target.value })}
                fullWidth
              />
            </VuiBox>
            
            <VuiBox mb={3}>
              <VuiTypography variant="caption" color="text" opacity={0.7} display="block" mb={1}>
                RTSP URL
              </VuiTypography>
              <VuiInput
                placeholder="rtsp://192.168.1.100:554/stream"
                value={formData.rtsp_url}
                onChange={(e) => setFormData({ ...formData, rtsp_url: e.target.value })}
                fullWidth
              />
            </VuiBox>
            
            <VuiBox mb={3}>
              <VuiTypography variant="caption" color="text" opacity={0.7} display="block" mb={1}>
                Initial Status
              </VuiTypography>
              <VuiInput
                select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                placeholder="Select status"
                fontWeight="500"
                sx={({ typography: { size } }) => ({
                  fontSize: size.sm,
                  color: 'white',
                  '& .MuiSelect-select': {
                    color: 'white',
                    padding: '12px 16px',
                  },
                  '& .MuiSvgIcon-root': {
                    color: 'white',
                  },
                })}
                icon={{
                  component: (
                    <VuiBox
                      display="flex"
                      alignItems="center"
                      gap={0.5}
                      px={1}
                      py={0.5}
                      borderRadius="sm"
                      bgColor={getStatusConfig(formData.status).bgColor}
                      color="white"
                    >
                      {getStatusConfig(formData.status).icon}
                      <VuiTypography variant="caption" color="white" fontWeight="medium" textTransform="capitalize">
                        {formData.status}
                      </VuiTypography>
                    </VuiBox>
                  ),
                  direction: 'right',
                }}
              >
                <option value="active">Active</option>
                <option value="offline">Offline</option>
                <option value="maintenance">Maintenance</option>
                <option value="error">Error</option>
              </VuiInput>
            </VuiBox>
          </VuiBox>
        </DialogContent>
        <DialogActions sx={{ 
          borderTop: '1px solid rgba(255,255,255,0.1)',
          pt: 2,
          px: 3,
          pb: 3
        }}>
          <VuiButton
            variant="outlined"
            onClick={() => setOpenAddDialog(false)}
            sx={{ mr: 1 }}
          >
            Cancel
          </VuiButton>
          <VuiButton
            color="info"
            variant="contained"
            onClick={handleAddCamera}
            startIcon={<IoAdd />}
          >
            Add Camera
          </VuiButton>
        </DialogActions>
      </Dialog>

      {/* Edit Camera Dialog */}
      <Dialog 
        open={openEditDialog} 
        onClose={() => setOpenEditDialog(false)} 
        maxWidth="sm" 
        fullWidth
        PaperProps={{
          sx: {
            backgroundColor: '#1a2035',
            color: 'white',
            borderRadius: '16px'
          }
        }}
      >
        <DialogTitle sx={{ 
          borderBottom: '1px solid rgba(255,255,255,0.1)',
          pb: 2
        }}>
          <VuiBox display="flex" alignItems="center">
            <VuiBox
              bgColor="warning"
              color="white"
              width="2.5rem"
              height="2.5rem"
              borderRadius="lg"
              display="flex"
              justifyContent="center"
              alignItems="center"
              mr={2}
            >
              <IoPencil size="20px" />
            </VuiBox>
            <VuiTypography variant="h6" color="white" fontWeight="bold">
              Edit Camera
            </VuiTypography>
          </VuiBox>
        </DialogTitle>
        <DialogContent sx={{ pt: 3 }}>
          <VuiBox>
            <VuiBox mb={3}>
              <VuiTypography variant="caption" color="text" opacity={0.7} display="block" mb={1}>
                Camera Name
              </VuiTypography>
              <TextField
                fullWidth
                placeholder="Enter camera name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    color: 'white',
                    '& fieldset': {
                      borderColor: 'rgba(255,255,255,0.2)'
                    },
                    '&:hover fieldset': {
                      borderColor: 'rgba(255,255,255,0.3)'
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#0075FF'
                    }
                  },
                  '& .MuiInputLabel-root': {
                    color: 'rgba(255,255,255,0.7)'
                  }
                }}
              />
            </VuiBox>
            
            <VuiBox mb={3}>
              <VuiTypography variant="caption" color="text" opacity={0.7} display="block" mb={1}>
                IP Address
              </VuiTypography>
              <VuiInput
                placeholder="192.168.1.100"
                value={formData.ip_address}
                onChange={(e) => setFormData({ ...formData, ip_address: e.target.value })}
                fullWidth
              />
            </VuiBox>
            
            <VuiBox mb={3}>
              <VuiTypography variant="caption" color="text" opacity={0.7} display="block" mb={1}>
                RTSP URL
              </VuiTypography>
              <VuiInput
                placeholder="rtsp://192.168.1.100:554/stream"
                value={formData.rtsp_url}
                onChange={(e) => setFormData({ ...formData, rtsp_url: e.target.value })}
                fullWidth
              />
            </VuiBox>
            
            <VuiBox mb={3}>
              <VuiTypography variant="caption" color="text" opacity={0.7} display="block" mb={1}>
                Status
              </VuiTypography>
              <VuiInput
                select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                placeholder="Select status"
                fontWeight="500"
                sx={({ typography: { size } }) => ({
                  fontSize: size.sm,
                  color: 'white',
                  '& .MuiSelect-select': {
                    color: 'white',
                    padding: '12px 16px',
                  },
                  '& .MuiSvgIcon-root': {
                    color: 'white',
                  },
                })}
                icon={{
                  component: (
                    <VuiBox
                      display="flex"
                      alignItems="center"
                      gap={0.5}
                      px={1}
                      py={0.5}
                      borderRadius="sm"
                      bgColor={getStatusConfig(formData.status).bgColor}
                      color="white"
                    >
                      {getStatusConfig(formData.status).icon}
                      <VuiTypography variant="caption" color="white" fontWeight="medium" textTransform="capitalize">
                        {formData.status}
                      </VuiTypography>
                    </VuiBox>
                  ),
                  direction: 'right',
                }}
              >
                <option value="active">Active</option>
                <option value="offline">Offline</option>
                <option value="maintenance">Maintenance</option>
                <option value="error">Error</option>
              </VuiInput>
            </VuiBox>
          </VuiBox>
        </DialogContent>
        <DialogActions sx={{ 
          borderTop: '1px solid rgba(255,255,255,0.1)',
          pt: 2,
          px: 3,
          pb: 3
        }}>
          <VuiButton
            variant="outlined"
            onClick={() => setOpenEditDialog(false)}
            sx={{ mr: 1 }}
          >
            Cancel
          </VuiButton>
          <VuiButton
            color="warning"
            variant="contained"
            onClick={handleEditCamera}
            startIcon={<IoPencil />}
          >
            Update Camera
          </VuiButton>
        </DialogActions>
      </Dialog>

      {/* Delete Camera Dialog */}
      <Dialog 
        open={openDeleteDialog} 
        onClose={() => setOpenDeleteDialog(false)}
        PaperProps={{
          sx: {
            backgroundColor: '#1a2035',
            color: 'white',
            borderRadius: '16px'
          }
        }}
      >
        <DialogTitle sx={{ 
          borderBottom: '1px solid rgba(255,255,255,0.1)',
          pb: 2
        }}>
          <VuiBox display="flex" alignItems="center">
            <VuiBox
              bgColor="error"
              color="white"
              width="2.5rem"
              height="2.5rem"
              borderRadius="lg"
              display="flex"
              justifyContent="center"
              alignItems="center"
              mr={2}
            >
              <IoClose size="20px" />
            </VuiBox>
            <VuiTypography variant="h6" color="white" fontWeight="bold">
              Delete Camera
            </VuiTypography>
          </VuiBox>
        </DialogTitle>
        <DialogContent sx={{ pt: 3 }}>
          <VuiBox>
            <VuiTypography variant="body1" color="white" mb={2}>
              Are you sure you want to delete <strong>"{selectedCamera?.name}"</strong>?
            </VuiTypography>
            <VuiTypography variant="body2" color="text" opacity={0.7}>
              This action cannot be undone and will permanently remove the camera from the system.
            </VuiTypography>
          </VuiBox>
        </DialogContent>
        <DialogActions sx={{ 
          borderTop: '1px solid rgba(255,255,255,0.1)',
          pt: 2,
          px: 3,
          pb: 3
        }}>
          <VuiButton
            variant="outlined"
            onClick={() => setOpenDeleteDialog(false)}
            sx={{ mr: 1 }}
          >
            Cancel
          </VuiButton>
          <VuiButton
            color="error"
            variant="contained"
            onClick={handleDeleteCamera}
            startIcon={<IoClose />}
          >
            Delete Camera
          </VuiButton>
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

    </DashboardLayout>
  );
}

export default Cameras; 