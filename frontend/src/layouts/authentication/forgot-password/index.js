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

import { useState } from "react";

// @mui material components
import { Link } from "react-router-dom";

// @mui icons
import FacebookIcon from "@mui/icons-material/Facebook";
import GoogleIcon from "@mui/icons-material/Google";

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiInput from "components/VuiInput";
import VuiButton from "components/VuiButton";
import VuiSwitch from "components/VuiSwitch";

// Vision UI Dashboard React example components
import CoverLayout from "../components/CoverLayout";

// Vision UI Dashboard assets
import radialGradient from "assets/theme/functions/radialGradient";
import palette from "assets/theme/base/colors";
import borders from "assets/theme/base/borders";

// Vision UI Dashboard theme components
import GradientBorder from "examples/GradientBorder";

// Images
import bgSignIn from "assets/images/signInImage.png";

function ForgotPassword() {
  const [formData, setFormData] = useState({
    email: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
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

    if (!formData.email.trim()) {
      newErrors.email = "Email là bắt buộc";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Email không hợp lệ";
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
      
      setSuccessMessage("Nếu email tồn tại, link đặt lại mật khẩu đã được gửi.");
      
    } catch (error) {
      setErrors({ submit: "Có lỗi xảy ra. Vui lòng thử lại." });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <CoverLayout
      title="Quên mật khẩu"
      color="white"
      description="Nhập email của bạn để nhận link đặt lại mật khẩu"
      premotto="CẢM HỨNG TỪ TƯƠNG LAI"
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
              type="email"
              name="email"
              value={formData.email}
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
          {errors.email && (
            <VuiTypography variant="caption" color="error" mt={0.5}>
              {errors.email}
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
            {isSubmitting ? "ĐANG GỬI..." : "GỬI LINK ĐẶT LẠI MẬT KHẨU"}
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

        <VuiBox mt={2} textAlign="center">
          <VuiTypography variant="button" color="text" fontWeight="regular">
            Chưa có tài khoản?{" "}
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
    </CoverLayout>
  );
}

export default ForgotPassword; 