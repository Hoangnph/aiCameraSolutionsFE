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

import { useState } from "react";

// @mui material components
import { Link, useLocation } from "react-router-dom";

// @mui icons
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiInput from "components/VuiInput";
import VuiButton from "components/VuiButton";

// Vision UI Dashboard React example components
import CoverLayout from "../components/CoverLayout";

// Vision UI Dashboard assets
import radialGradient from "assets/theme/functions/radialGradient";
import palette from "assets/theme/base/colors";
import borders from "assets/theme/base/borders";

// Vision UI Dashboard theme components
import GradientBorder from "examples/GradientBorder";

function ResetPassword() {
  const location = useLocation();
  
  // Lấy token từ URL nếu có (từ email reset)
  const searchParams = new URLSearchParams(location.search);
  const token = searchParams.get('token');
  
  const [formData, setFormData] = useState({
    password: "",
    confirmPassword: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState("");

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

    if (!formData.password) {
      newErrors.password = "Mật khẩu là bắt buộc";
    } else if (formData.password.length < 8) {
      newErrors.password = "Mật khẩu phải có ít nhất 8 ký tự";
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/.test(formData.password)) {
      newErrors.password = "Mật khẩu phải chứa chữ hoa, chữ thường, số và ký tự đặc biệt";
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = "Vui lòng xác nhận mật khẩu";
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Mật khẩu không khớp";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccessMessage("");
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (token) {
        // Reset password với token (từ email)
        setSuccessMessage("Đặt lại mật khẩu thành công! Bạn có thể đăng nhập với mật khẩu mới.");
      } else {
        // Change password (từ profile)
        setSuccessMessage("Đổi mật khẩu thành công!");
      }
      
    } catch (error) {
      setErrors({ submit: "Có lỗi xảy ra. Vui lòng thử lại." });
    } finally {
      setIsSubmitting(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  // Nếu không có token và không phải từ profile (có thể là truy cập trực tiếp)
  if (!token) {
    return (
      <CoverLayout
        title="Đặt lại mật khẩu"
        description="Nhập mật khẩu mới cho tài khoản của bạn"
        image="https://images.unsplash.com/photo-1497294815431-9365093b7331?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1950&q=80"
      >
        <VuiBox component="form" role="form" onSubmit={handleSubmit}>
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
            <VuiBox
              borderRadius={borders.borderRadius.lg}
              padding="2rem"
              bgColor="info"
              sx={{
                backgroundImage: radialGradient(
                  palette.gradients.info.main,
                  palette.gradients.info.state,
                  palette.gradients.info.angle
                ),
              }}
            >
              {successMessage && (
                <VuiBox mb={2}>
                  <VuiTypography variant="button" color="success" fontWeight="medium">
                    {successMessage}
                  </VuiTypography>
                </VuiBox>
              )}

              {errors.submit && (
                <VuiBox mb={2}>
                  <VuiTypography variant="button" color="error" fontWeight="medium">
                    {errors.submit}
                  </VuiTypography>
                </VuiBox>
              )}

              <VuiBox mb={2}>
                <VuiBox mb={1} ml={0.5}>
                  <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
                    Mật khẩu mới
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
                    placeholder="Nhập mật khẩu mới"
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
                    error={!!errors.password}
                  />
                </GradientBorder>
                {errors.password && (
                  <VuiTypography variant="caption" color="error" mt={0.5}>
                    {errors.password}
                  </VuiTypography>
                )}
              </VuiBox>

              <VuiBox mb={2}>
                <VuiBox mb={1} ml={0.5}>
                  <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
                    Xác nhận mật khẩu mới
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
                    placeholder="Nhập lại mật khẩu mới"
                    sx={({ typography: { size } }) => ({
                      fontSize: size.sm,
                      color: 'white',
                    })}
                    required
                    icon={{
                      component: (
                        <span onClick={toggleConfirmPasswordVisibility} style={{ cursor: 'pointer', color: 'white', display: 'flex', alignItems: 'center' }}>
                          {showConfirmPassword ? <Visibility /> : <VisibilityOff />}
                        </span>
                      ),
                      direction: 'left',
                    }}
                    error={!!errors.confirmPassword}
                  />
                </GradientBorder>
                {errors.confirmPassword && (
                  <VuiTypography variant="caption" color="error" mt={0.5}>
                    {errors.confirmPassword}
                  </VuiTypography>
                )}
              </VuiBox>

              <VuiBox mt={4} mb={1}>
                <VuiButton 
                  color="info" 
                  fullWidth 
                  type="submit"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? "ĐANG ĐẶT LẠI..." : "ĐẶT LẠI MẬT KHẨU"}
                </VuiButton>
              </VuiBox>

              <VuiBox mt={3} textAlign="center">
                <VuiTypography variant="button" color="text" fontWeight="regular">
                  Nhớ mật khẩu?{" "}
                  <VuiTypography
                    component={Link}
                    to="/authentication/sign-in"
                    variant="button"
                    color="white"
                    fontWeight="medium"
                  >
                    Đăng nhập
                  </VuiTypography>
                </VuiTypography>
              </VuiBox>
            </VuiBox>
          </GradientBorder>
        </VuiBox>
      </CoverLayout>
    );
  }

  // Nếu có token (từ email reset)
  return (
    <CoverLayout
      title="Đặt lại mật khẩu"
      description="Nhập mật khẩu mới cho tài khoản của bạn"
      image="https://images.unsplash.com/photo-1497294815431-9365093b7331?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1950&q=80"
    >
      <VuiBox component="form" role="form" onSubmit={handleSubmit}>
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
          <VuiBox
            borderRadius={borders.borderRadius.lg}
            padding="2rem"
            bgColor="info"
            sx={{
              backgroundImage: radialGradient(
                palette.gradients.info.main,
                palette.gradients.info.state,
                palette.gradients.info.angle
              ),
            }}
          >
            {successMessage && (
              <VuiBox mb={2}>
                <VuiTypography variant="button" color="success" fontWeight="medium">
                  {successMessage}
                </VuiTypography>
              </VuiBox>
            )}

            {errors.submit && (
              <VuiBox mb={2}>
                <VuiTypography variant="button" color="error" fontWeight="medium">
                  {errors.submit}
                </VuiTypography>
              </VuiBox>
            )}

            <VuiBox mb={2}>
              <VuiBox mb={1} ml={0.5}>
                <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
                  Mật khẩu mới
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
                  placeholder="Nhập mật khẩu mới"
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
                  error={!!errors.password}
                />
              </GradientBorder>
              {errors.password && (
                <VuiTypography variant="caption" color="error" mt={0.5}>
                  {errors.password}
                </VuiTypography>
              )}
            </VuiBox>

            <VuiBox mb={2}>
              <VuiBox mb={1} ml={0.5}>
                <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
                  Xác nhận mật khẩu mới
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
                  placeholder="Nhập lại mật khẩu mới"
                  sx={({ typography: { size } }) => ({
                    fontSize: size.sm,
                    color: 'white',
                  })}
                  required
                  icon={{
                    component: (
                      <span onClick={toggleConfirmPasswordVisibility} style={{ cursor: 'pointer', color: 'white', display: 'flex', alignItems: 'center' }}>
                        {showConfirmPassword ? <Visibility /> : <VisibilityOff />}
                      </span>
                    ),
                    direction: 'left',
                  }}
                  error={!!errors.confirmPassword}
                />
              </GradientBorder>
              {errors.confirmPassword && (
                <VuiTypography variant="caption" color="error" mt={0.5}>
                  {errors.confirmPassword}
                </VuiTypography>
              )}
            </VuiBox>

            <VuiBox mt={4} mb={1}>
              <VuiButton 
                color="info" 
                fullWidth 
                type="submit"
                disabled={isSubmitting}
              >
                {isSubmitting ? "ĐANG ĐẶT LẠI..." : "ĐẶT LẠI MẬT KHẨU"}
              </VuiButton>
            </VuiBox>

            <VuiBox mt={3} textAlign="center">
              <VuiTypography variant="button" color="text" fontWeight="regular">
                Nhớ mật khẩu?{" "}
                <VuiTypography
                  component={Link}
                  to="/authentication/sign-in"
                  variant="button"
                  color="white"
                  fontWeight="medium"
                >
                  Đăng nhập
                </VuiTypography>
              </VuiTypography>
            </VuiBox>
          </VuiBox>
        </GradientBorder>
      </VuiBox>
    </CoverLayout>
  );
}

export default ResetPassword; 