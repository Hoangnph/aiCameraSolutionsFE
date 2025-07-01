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
import { useHistory } from "react-router-dom";

// react-router-dom components
import { Link } from "react-router-dom";

// @mui material components
import Icon from "@mui/material/Icon";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';

// Icons
import { FaApple, FaFacebook, FaGoogle } from "react-icons/fa";

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiInput from "components/VuiInput";
import VuiButton from "components/VuiButton";
import VuiSwitch from "components/VuiSwitch";
import GradientBorder from "examples/GradientBorder";

// Vision UI Dashboard assets
import radialGradient from "assets/theme/functions/radialGradient";
import rgba from "assets/theme/functions/rgba";
import palette from "assets/theme/base/colors";
import borders from "assets/theme/base/borders";

// Authentication layout components
import CoverLayout from "layouts/authentication/components/CoverLayout";

// Authentication context
import { useAuth } from "context/AuthContext";

// Images
import bgSignIn from "assets/images/signUpImage.png";

function SignUp() {
  const [rememberMe, setRememberMe] = useState(true);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    firstName: "",
    lastName: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [backendError, setBackendError] = useState("");
  const [backendFieldErrors, setBackendFieldErrors] = useState({});
  const [openErrorModal, setOpenErrorModal] = useState(false);
  const [showSnackbar, setShowSnackbar] = useState(false);

  const { register, error, clearError } = useAuth();
  const history = useHistory();

  // Debug useEffect to monitor state changes
  useEffect(() => {
    // Monitor state changes for debugging
  }, [openErrorModal, backendError]);

  const handleSetRememberMe = () => setRememberMe(!rememberMe);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ""
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.username.trim()) {
      newErrors.username = "Username is required";
    } else if (formData.username.length < 3) {
      newErrors.username = "Username must be at least 3 characters";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Email is invalid";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/.test(formData.password)) {
      newErrors.password = "Password must contain uppercase, lowercase, number and special character";
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = "Please confirm your password";
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    if (!formData.firstName.trim()) {
      newErrors.firstName = "First name is required";
    } else if (formData.firstName.length < 2) {
      newErrors.firstName = "First name must be at least 2 characters";
    }

    if (!formData.lastName.trim()) {
      newErrors.lastName = "Last name is required";
    } else if (formData.lastName.length < 2) {
      newErrors.lastName = "Last name must be at least 2 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setBackendError("");
    setBackendFieldErrors({});
    if (!validateForm()) {
      return;
    }
    setIsSubmitting(true);
    try {
      const result = await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        confirmPassword: formData.confirmPassword,
        firstName: formData.firstName,
        lastName: formData.lastName,
      });
      if (result.success) {
        history.replace("/dashboard");
      }
    } catch (error) {
      console.log('DEBUG: Full error object:', error);
      console.log('DEBUG: Error type:', typeof error);
      console.log('DEBUG: Error keys:', Object.keys(error));
      
      // Simplify error handling
      let errorMessage = "Đăng ký thất bại. Vui lòng thử lại.";
      let fieldErrors = {};
      
      if (error && typeof error === "object") {
        // Handle the specific backend error structure
        if (error.error && error.error.message) {
          errorMessage = error.error.message;
        } else if (error.message) {
          errorMessage = error.message;
        } else if (typeof error.error === "string") {
          errorMessage = error.error;
        }
        
        // Try different field error sources
        if (error.error && error.error.details) {
          fieldErrors = error.error.details;
        } else if (error.details) {
          fieldErrors = error.details;
        }
      }
      
      console.log('DEBUG: Final error message:', errorMessage);
      console.log('DEBUG: Final field errors:', fieldErrors);
      
      setBackendError(errorMessage);
      setBackendFieldErrors(fieldErrors);
      setOpenErrorModal(true);
      setShowSnackbar(true);
      
      console.log('DEBUG: States set - openErrorModal:', true, 'showSnackbar:', true);
      setTimeout(() => {
        console.log('DEBUG: Timeout check openErrorModal', openErrorModal, backendError);
      }, 100);
    }
    setIsSubmitting(false);
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  return (
    <>
      {/* Modal lỗi sử dụng MUI Dialog */}
      <Dialog
        open={openErrorModal}
        onClose={() => setOpenErrorModal(false)}
        aria-labelledby="error-dialog-title"
        aria-describedby="error-dialog-description"
        PaperProps={{
          sx: {
            borderRadius: 4,
            minWidth: 320,
            maxWidth: '90%',
            background: '#fff',
            boxShadow: '0 8px 32px rgba(0,0,0,0.18)',
            p: 0
          }
        }}
      >
        <DialogTitle id="error-dialog-title" sx={{ color: '#111', fontWeight: 700, fontSize: 22, textAlign: 'center', pb: 0 }}>
          Đăng ký thất bại
        </DialogTitle>
        <DialogContent sx={{ color: '#111', fontSize: 16, textAlign: 'center', pt: 1, pb: 0 }}>
          {backendError}
        </DialogContent>
        <DialogActions sx={{ justifyContent: 'center', pb: 2, pt: 2 }}>
          <Button
            onClick={() => setOpenErrorModal(false)}
            variant="contained"
            sx={{
              borderRadius: 99,
              px: 4,
              py: 1.2,
              fontWeight: 600,
              fontSize: 16,
              background: 'linear-gradient(90deg,#5e72e4,#825ee4)',
              color: '#fff',
              boxShadow: '0 2px 8px rgba(94,114,228,0.12)',
              '&:hover': {
                background: 'linear-gradient(90deg,#825ee4,#5e72e4)'
              }
            }}
          >
            Đóng
          </Button>
        </DialogActions>
      </Dialog>

      {/* Optional: Snackbar for quick error notification */}
      <Snackbar
        open={showSnackbar}
        autoHideDuration={4000}
        onClose={() => setShowSnackbar(false)}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert severity="error" sx={{ width: '100%' }}>
          {backendError}
        </Alert>
      </Snackbar>

      <CoverLayout
        title="Welcome!"
        color="white"
        description="Create your account to get started with our platform."
        image={bgSignIn}
        premotto="INSPIRED BY THE FUTURE:"
        motto="THE VISION UI DASHBOARD"
        cardContent
      >
        <GradientBorder borderRadius={borders.borderRadius.form} minWidth="100%" maxWidth="100%">
          <VuiBox
            component="form"
            role="form"
            borderRadius="inherit"
            p="45px"
            onSubmit={handleSubmit}
            sx={({ palette: { secondary } }) => ({
              backgroundColor: secondary.focus,
            })}
          >
            <VuiTypography
              color="white"
              fontWeight="bold"
              textAlign="center"
              mb="24px"
              sx={({ typography: { size } }) => ({
                fontSize: size.lg,
              })}
            >
              Register with
            </VuiTypography>
            
            <Stack mb="25px" justifyContent="center" alignItems="center" direction="row" spacing={2}>
              <GradientBorder borderRadius="xl">
                <a href="#">
                  <IconButton
                    transition="all .25s ease"
                    justify="center"
                    align="center"
                    bg="rgb(19,21,54)"
                    borderradius="15px"
                    sx={({ palette: { secondary }, borders: { borderRadius } }) => ({
                      borderRadius: borderRadius.xl,
                      padding: "25px",
                      backgroundColor: secondary.focus,
                      "&:hover": {
                        backgroundColor: rgba(secondary.focus, 0.9),
                      },
                    })}
                  >
                    <Icon
                      as={FaFacebook}
                      w="30px"
                      h="30px"
                      sx={({ palette: { white } }) => ({
                        color: white.focus,
                      })}
                    />
                  </IconButton>
                </a>
              </GradientBorder>
              <GradientBorder borderRadius="xl">
                <a href="#">
                  <IconButton
                    transition="all .25s ease"
                    justify="center"
                    align="center"
                    bg="rgb(19,21,54)"
                    borderradius="15px"
                    sx={({ palette: { secondary }, borders: { borderRadius } }) => ({
                      borderRadius: borderRadius.xl,
                      padding: "25px",
                      backgroundColor: secondary.focus,
                      "&:hover": {
                        backgroundColor: rgba(secondary.focus, 0.9),
                      },
                    })}
                  >
                    <Icon
                      as={FaApple}
                      w="30px"
                      h="30px"
                      sx={({ palette: { white } }) => ({
                        color: white.focus,
                      })}
                    />
                  </IconButton>
                </a>
              </GradientBorder>
              <GradientBorder borderRadius="xl">
                <a href="#">
                  <IconButton
                    transition="all .25s ease"
                    justify="center"
                    align="center"
                    bg="rgb(19,21,54)"
                    borderradius="15px"
                    sx={({ palette: { secondary }, borders: { borderRadius } }) => ({
                      borderRadius: borderRadius.xl,
                      padding: "25px",
                      backgroundColor: secondary.focus,
                      "&:hover": {
                        backgroundColor: rgba(secondary.focus, 0.9),
                      },
                    })}
                  >
                    <Icon
                      as={FaGoogle}
                      w="30px"
                      h="30px"
                      sx={({ palette: { white } }) => ({
                        color: white.focus,
                      })}
                    />
                  </IconButton>
                </a>
              </GradientBorder>
            </Stack>
            
            <VuiTypography
              color="text"
              fontWeight="bold"
              textAlign="center"
              mb="14px"
              sx={({ typography: { size } }) => ({ fontSize: size.lg })}
            >
              or
            </VuiTypography>
            
            <VuiBox mb={2}>
              <VuiBox mb={1} ml={0.5}>
                <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
                  First Name
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
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleInputChange}
                  placeholder="Your first name..."
                  sx={({ typography: { size } }) => ({
                    fontSize: size.sm,
                  })}
                  required
                  error={!!errors.firstName || !!backendFieldErrors.firstName}
                />
              </GradientBorder>
              {errors.firstName && (
                <VuiTypography variant="caption" color="error" mt={0.5}>
                  {errors.firstName}
                </VuiTypography>
              )}
              {backendFieldErrors.firstName && (
                <div style={{ color: 'red', fontSize: 13 }}>{backendFieldErrors.firstName}</div>
              )}
            </VuiBox>

            <VuiBox mb={2}>
              <VuiBox mb={1} ml={0.5}>
                <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
                  Last Name
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
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleInputChange}
                  placeholder="Your last name..."
                  sx={({ typography: { size } }) => ({
                    fontSize: size.sm,
                  })}
                  required
                  error={!!errors.lastName || !!backendFieldErrors.lastName}
                />
              </GradientBorder>
              {errors.lastName && (
                <VuiTypography variant="caption" color="error" mt={0.5}>
                  {errors.lastName}
                </VuiTypography>
              )}
              {backendFieldErrors.lastName && (
                <div style={{ color: 'red', fontSize: 13 }}>{backendFieldErrors.lastName}</div>
              )}
            </VuiBox>

            <VuiBox mb={2}>
              <VuiBox mb={1} ml={0.5}>
                <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
                  Username
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
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  placeholder="Your username..."
                  sx={({ typography: { size } }) => ({
                    fontSize: size.sm,
                  })}
                  required
                  error={!!errors.username || !!backendFieldErrors.username}
                />
              </GradientBorder>
              {errors.username && (
                <VuiTypography variant="caption" color="error" mt={0.5}>
                  {errors.username}
                </VuiTypography>
              )}
              {backendFieldErrors.username && (
                <div style={{ color: 'red', fontSize: 13 }}>{backendFieldErrors.username}</div>
              )}
            </VuiBox>

            <VuiBox mb={2}>
              <VuiBox mb={1} ml={0.5}>
                <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
                  Email
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
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="Your email..."
                  sx={({ typography: { size } }) => ({
                    fontSize: size.sm,
                  })}
                  required
                  error={!!errors.email || !!backendFieldErrors.email}
                />
              </GradientBorder>
              {errors.email && (
                <VuiTypography variant="caption" color="error" mt={0.5}>
                  {errors.email}
                </VuiTypography>
              )}
              {backendFieldErrors.email && (
                <div style={{ color: 'red', fontSize: 13 }}>{backendFieldErrors.email}</div>
              )}
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
                  placeholder="Your password..."
                  sx={({ typography: { size } }) => ({
                    fontSize: size.sm,
                  })}
                  required
                  endAdornment={
                    <VuiBox
                      component="span"
                      onClick={togglePasswordVisibility}
                      sx={{ cursor: "pointer", color: "white" }}
                    >
                      {showPassword ? "👁️" : "👁️‍🗨️"}
                    </VuiBox>
                  }
                  error={!!errors.password || !!backendFieldErrors.password}
                />
              </GradientBorder>
              {errors.password && (
                <VuiTypography variant="caption" color="error" mt={0.5}>
                  {errors.password}
                </VuiTypography>
              )}
              {backendFieldErrors.password && (
                <div style={{ color: 'red', fontSize: 13 }}>{backendFieldErrors.password}</div>
              )}
            </VuiBox>

            <VuiBox mb={2}>
              <VuiBox mb={1} ml={0.5}>
                <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
                  Confirm Password
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
                  type={showConfirmPassword ? "text" : "password"}
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  placeholder="Confirm your password..."
                  sx={({ typography: { size } }) => ({
                    fontSize: size.sm,
                  })}
                  required
                  endAdornment={
                    <VuiBox
                      component="span"
                      onClick={toggleConfirmPasswordVisibility}
                      sx={{ cursor: "pointer", color: "white" }}
                    >
                      {showConfirmPassword ? "👁️" : "👁️‍🗨️"}
                    </VuiBox>
                  }
                  error={!!errors.confirmPassword || !!backendFieldErrors.confirmPassword}
                />
              </GradientBorder>
              {errors.confirmPassword && (
                <VuiTypography variant="caption" color="error" mt={0.5}>
                  {errors.confirmPassword}
                </VuiTypography>
              )}
              {backendFieldErrors.confirmPassword && (
                <div style={{ color: 'red', fontSize: 13 }}>{backendFieldErrors.confirmPassword}</div>
              )}
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
                &nbsp;&nbsp;&nbsp;&nbsp;I agree to the terms and conditions
              </VuiTypography>
            </VuiBox>

            <VuiBox mt={4} mb={1}>
              <VuiButton 
                color="info" 
                fullWidth 
                type="submit"
                disabled={isSubmitting}
              >
                {isSubmitting ? "CREATING ACCOUNT..." : "SIGN UP"}
              </VuiButton>
            </VuiBox>

            <VuiBox mt={3} textAlign="center">
              <VuiTypography variant="button" color="text" fontWeight="regular">
                Already have an account?{" "}
                <VuiTypography
                  component={Link}
                  to="/authentication/sign-in"
                  variant="button"
                  color="white"
                  fontWeight="medium"
                >
                  Sign in
                </VuiTypography>
              </VuiTypography>
            </VuiBox>
          </VuiBox>
        </GradientBorder>
      </CoverLayout>
    </>
  );
}

export default SignUp;
