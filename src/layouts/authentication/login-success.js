import React from 'react';
import { useHistory } from 'react-router-dom';
import VuiBox from 'components/VuiBox';
import VuiTypography from 'components/VuiTypography';
import VuiButton from 'components/VuiButton';

const LoginSuccess = () => {
  const history = useHistory();
  return (
    <VuiBox display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="100vh">
      <VuiTypography variant="h3" color="success" mb={2}>
        Đăng nhập thành công!
      </VuiTypography>
      <VuiTypography variant="body1" mb={4}>
        Bạn đã đăng nhập thành công vào hệ thống.
      </VuiTypography>
      <VuiButton color="primary" onClick={() => history.push('/dashboard')}>
        Vào trang Dashboard
      </VuiButton>
    </VuiBox>
  );
};

export default LoginSuccess; 