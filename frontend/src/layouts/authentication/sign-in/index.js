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

import { useState, useEffect } from "react";
import { useHistory, useLocation } from "react-router-dom";

// react-router-dom components
import { Link } from "react-router-dom";

// @mui material components
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiInput from "components/VuiInput";
import VuiButton from "components/VuiButton";
import VuiSwitch from "components/VuiSwitch";
import GradientBorder from "examples/GradientBorder";

// Vision UI Dashboard assets
import radialGradient from "assets/theme/functions/radialGradient";
import palette from "assets/theme/base/colors";
import borders from "assets/theme/base/borders";

// Authentication layout components
import CoverLayout from "layouts/authentication/components/CoverLayout";

// Authentication context
import { useAuth } from "context/AuthContext";

// Images
import bgSignIn from "assets/images/signInImage.png";

import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';

function SignIn() {
  const [rememberMe, setRememberMe] = useState(true);
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [openErrorModal, setOpenErrorModal] = useState(false);
  const [showSnackbar, setShowSnackbar] = useState(false);

  const { login } = useAuth();
  const history = useHistory();
  const location = useLocation();

  const handleSetRememberMe = () => setRememberMe(!rememberMe);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    if (!formData.username || !formData.password) {
      setLoading(false);
      return;
    }

    try {
      await login(formData);
      setLoading(false);
      // Chuyển hướng thẳng đến dashboard
      history.push('/dashboard');
    } catch (err) {
      setLoading(false);
      setError(err.message || 'Đăng nhập thất bại');
      setOpenErrorModal(true);
      setShowSnackbar(true);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <CoverLayout
      title="Chào mừng bạn."
      color="white"
      description="Cho tôi biết email và password của bạn để đăng nhập nhé"
      premotto="CẢM HỨNG TỪ TƯƠNG LAI"
      motto="aiCamera Solutions"
      image={bgSignIn}
      hideNavbar={true}
      hideFooter={true}
    >
      <VuiBox component="form" role="form" onSubmit={handleSubmit}>
        <VuiBox mb={2}>
          <VuiBox mb={1} ml={0.5}>
            <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
              Email
            </VuiTypography>
          </VuiBox>
          <GradientBorder
            minWidth="100%"
            padding="1px"
            borderRadius={borders.borderRadius.lg}
            backgroundImage={radialGradient(
              palette.gradients.borderLight.main,
              palette.gradients.borderLight.state,
              palette.gradients.borderLight.angle
            )}
          >
            <VuiInput
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder="Nhập email của bạn vào đây"
              fontWeight="500"
              required
              sx={({ typography: { size } }) => ({
                fontSize: size.sm,
                color: 'white',
              })}
            />
          </GradientBorder>
        </VuiBox>
        
        <VuiBox mb={2}>
          <VuiBox mb={1} ml={0.5}>
            <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
              Password
            </VuiTypography>
          </VuiBox>
          <GradientBorder
            minWidth="100%"
            borderRadius={borders.borderRadius.lg}
            padding="1px"
            backgroundImage={radialGradient(
              palette.gradients.borderLight.main,
              palette.gradients.borderLight.state,
              palette.gradients.borderLight.angle
            )}
          >
            <VuiInput
              type={showPassword ? "text" : "password"}
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Nhập password của bạn vào đây"
              sx={({ typography: { size } }) => ({
                fontSize: size.sm,
                color: 'white',
              })}
              required
              icon={{
                component: (
                  <span onClick={togglePasswordVisibility} style={{ cursor: 'pointer', color: 'white', display: 'flex', alignItems: 'center' }}>
                    {showPassword ? <Visibility /> : <VisibilityOff />}
                  </span>
                ),
                direction: 'left',
              }}
            />
          </GradientBorder>
        </VuiBox>
        
        <VuiBox display="flex" alignItems="center">
          <VuiSwitch color="info" checked={rememberMe} onChange={handleSetRememberMe} />
          <VuiTypography
            variant="caption"
            color="white"
            fontWeight="medium"
            onClick={handleSetRememberMe}
            sx={{ cursor: "pointer", userSelect: "none" }}
          >
            &nbsp;&nbsp;&nbsp;&nbsp;Lưu lại thông tin đăng nhập
          </VuiTypography>
        </VuiBox>
        
        <VuiBox mt={4} mb={1}>
          <VuiButton 
            color="info" 
            fullWidth 
            type="submit"
            disabled={isSubmitting || !formData.username || !formData.password}
          >
            {loading ? "ĐANG ĐĂNG NHẬP..." : "ĐĂNG NHẬP"}
          </VuiButton>
        </VuiBox>
        
        <VuiBox mt={3} textAlign="center">
          <VuiTypography variant="button" color="text" fontWeight="regular">
            Bạn đã có tài khoản chưa?{" "}
            <VuiTypography
              component={Link}
              to="/authentication/sign-up"
              variant="button"
              color="white"
              fontWeight="medium"
            >
              Đăng ký
            </VuiTypography>
          </VuiTypography>
        </VuiBox>
      </VuiBox>
      
      {/* Error Modal - moved outside form to ensure proper rendering */}
      <Dialog 
        open={openErrorModal && !!error} 
        onClose={() => setOpenErrorModal(false)}
        PaperProps={{
          sx: {
            backgroundColor: 'white',
            borderRadius: 2,
            minWidth: 400,
            maxWidth: 600
          }
        }}
      >
        <DialogTitle sx={{ 
          backgroundColor: '#d32f2f', 
          color: 'white',
          fontWeight: 'bold'
        }}>
          Lỗi đăng nhập
        </DialogTitle>
        <DialogContent sx={{ pt: 3, pb: 2 }}>
          <div style={{ 
            color: '#d32f2f', 
            fontWeight: 600, 
            fontSize: 16,
            lineHeight: 1.5
          }}>
            {error}
          </div>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button 
            onClick={() => setOpenErrorModal(false)} 
            variant="contained" 
            color="primary" 
            autoFocus
            sx={{ 
              backgroundColor: '#1976d2',
              '&:hover': {
                backgroundColor: '#1565c0'
              }
            }}
          >
            Đóng
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Alternative error display using Snackbar */}
      <Snackbar
        open={showSnackbar}
        autoHideDuration={6000}
        onClose={() => setShowSnackbar(false)}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert 
          onClose={() => setShowSnackbar(false)} 
          severity="error" 
          sx={{ width: '100%' }}
        >
          {error}
        </Alert>
      </Snackbar>
    </CoverLayout>
  );
}

export default SignIn;
