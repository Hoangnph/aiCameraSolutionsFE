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
import { Link, useHistory } from "react-router-dom";

// @mui icons
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiInput from "components/VuiInput";
import VuiButton from "components/VuiButton";
import GradientBorder from "examples/GradientBorder";

// Vision UI Dashboard assets
import radialGradient from "assets/theme/functions/radialGradient";
import palette from "assets/theme/base/colors";
import borders from "assets/theme/base/borders";

// Authentication layout components
import CoverLayout from "layouts/authentication/components/CoverLayout";

// Auth context
import { useAuth } from "context/AuthContext";

// Images
import bgSignIn from "assets/images/signInImage.png";

function ChangePassword() {
  const history = useHistory();
  const { changePassword } = useAuth();
  
  const [formData, setFormData] = useState({
    currentPassword: "",
    newPassword: "",
    confirmNewPassword: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
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

    if (!formData.currentPassword) {
      newErrors.currentPassword = "Mật khẩu hiện tại là bắt buộc";
    }

    if (!formData.newPassword) {
      newErrors.newPassword = "Mật khẩu mới là bắt buộc";
    } else if (formData.newPassword.length < 8) {
      newErrors.newPassword = "Mật khẩu mới phải có ít nhất 8 ký tự";
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/.test(formData.newPassword)) {
      newErrors.newPassword = "Mật khẩu mới phải chứa chữ hoa, chữ thường, số và ký tự đặc biệt";
    }

    if (!formData.confirmNewPassword) {
      newErrors.confirmNewPassword = "Vui lòng xác nhận mật khẩu mới";
    } else if (formData.newPassword !== formData.confirmNewPassword) {
      newErrors.confirmNewPassword = "Mật khẩu mới không khớp";
    }

    // Kiểm tra mật khẩu mới không được giống mật khẩu cũ
    if (formData.currentPassword && formData.newPassword && formData.currentPassword === formData.newPassword) {
      newErrors.newPassword = "Mật khẩu mới không được giống mật khẩu hiện tại";
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
      const result = await changePassword({
        currentPassword: formData.currentPassword,
        newPassword: formData.newPassword,
        confirmNewPassword: formData.confirmNewPassword
      });
      
      if (result.success) {
        setSuccessMessage(result.message || "Đổi mật khẩu thành công!");
        
        // Redirect về profile sau 2 giây
        setTimeout(() => {
          history.push("/profile");
        }, 2000);
      } else {
        setErrors({ submit: result.error || "Có lỗi xảy ra. Vui lòng thử lại." });
      }
      
    } catch (error) {
      setErrors({ submit: error.message || "Có lỗi xảy ra. Vui lòng thử lại." });
    } finally {
      setIsSubmitting(false);
    }
  };

  const toggleCurrentPasswordVisibility = () => {
    setShowCurrentPassword(!showCurrentPassword);
  };

  const toggleNewPasswordVisibility = () => {
    setShowNewPassword(!showNewPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  return (
    <CoverLayout
      title="Đổi mật khẩu"
      color="white"
      description="Nhập mật khẩu hiện tại và mật khẩu mới để cập nhật tài khoản của bạn"
      premotto="BẢO MẬT TÀI KHOẢN"
      motto="aiCamera Solutions"
      image={bgSignIn}
      hideNavbar={true}
      hideFooter={true}
    >
      <VuiBox component="form" role="form" onSubmit={handleSubmit}>
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

        {/* Mật khẩu hiện tại */}
        <VuiBox mb={2}>
          <VuiBox mb={1} ml={0.5}>
            <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
              Mật khẩu hiện tại
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
              type={showCurrentPassword ? "text" : "password"}
              name="currentPassword"
              value={formData.currentPassword}
              onChange={handleInputChange}
              placeholder="Nhập mật khẩu hiện tại"
              fontWeight="500"
              required
              sx={({ typography: { size } }) => ({
                fontSize: size.sm,
                color: 'white',
              })}
              icon={{
                component: (
                  <span onClick={toggleCurrentPasswordVisibility} style={{ cursor: 'pointer', color: 'white', display: 'flex', alignItems: 'center' }}>
                    {showCurrentPassword ? <Visibility /> : <VisibilityOff />}
                  </span>
                ),
                direction: 'left',
              }}
              error={!!errors.currentPassword}
            />
          </GradientBorder>
          {errors.currentPassword && (
            <VuiTypography variant="caption" color="error" mt={0.5}>
              {errors.currentPassword}
            </VuiTypography>
          )}
        </VuiBox>

        {/* Mật khẩu mới */}
        <VuiBox mb={2}>
          <VuiBox mb={1} ml={0.5}>
            <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
              Mật khẩu mới
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
              type={showNewPassword ? "text" : "password"}
              name="newPassword"
              value={formData.newPassword}
              onChange={handleInputChange}
              placeholder="Nhập mật khẩu mới"
              fontWeight="500"
              required
              sx={({ typography: { size } }) => ({
                fontSize: size.sm,
                color: 'white',
              })}
              icon={{
                component: (
                  <span onClick={toggleNewPasswordVisibility} style={{ cursor: 'pointer', color: 'white', display: 'flex', alignItems: 'center' }}>
                    {showNewPassword ? <Visibility /> : <VisibilityOff />}
                  </span>
                ),
                direction: 'left',
              }}
              error={!!errors.newPassword}
            />
          </GradientBorder>
          {errors.newPassword && (
            <VuiTypography variant="caption" color="error" mt={0.5}>
              {errors.newPassword}
            </VuiTypography>
          )}
        </VuiBox>

        {/* Xác nhận mật khẩu mới */}
        <VuiBox mb={2}>
          <VuiBox mb={1} ml={0.5}>
            <VuiTypography component="label" variant="button" color="white" fontWeight="medium">
              Xác nhận mật khẩu mới
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
              type={showConfirmPassword ? "text" : "password"}
              name="confirmNewPassword"
              value={formData.confirmNewPassword}
              onChange={handleInputChange}
              placeholder="Nhập lại mật khẩu mới"
              fontWeight="500"
              required
              sx={({ typography: { size } }) => ({
                fontSize: size.sm,
                color: 'white',
              })}
              icon={{
                component: (
                  <span onClick={toggleConfirmPasswordVisibility} style={{ cursor: 'pointer', color: 'white', display: 'flex', alignItems: 'center' }}>
                    {showConfirmPassword ? <Visibility /> : <VisibilityOff />}
                  </span>
                ),
                direction: 'left',
              }}
              error={!!errors.confirmNewPassword}
            />
          </GradientBorder>
          {errors.confirmNewPassword && (
            <VuiTypography variant="caption" color="error" mt={0.5}>
              {errors.confirmNewPassword}
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
            {isSubmitting ? "ĐANG ĐỔI MẬT KHẨU..." : "ĐỔI MẬT KHẨU"}
          </VuiButton>
        </VuiBox>

        <VuiBox mt={3} textAlign="center">
          <VuiTypography variant="button" color="text" fontWeight="regular">
            Quay lại{" "}
            <VuiTypography
              component={Link}
              to="/profile"
              variant="button"
              color="white"
              fontWeight="medium"
            >
              Profile
            </VuiTypography>
          </VuiTypography>
        </VuiBox>
      </VuiBox>
    </CoverLayout>
  );
}

export default ChangePassword; 