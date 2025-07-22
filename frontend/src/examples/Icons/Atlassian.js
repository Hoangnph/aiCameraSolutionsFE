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

// prop-types is a library for typechecking of props
import PropTypes from "prop-types";

function Atlassian({ size = "16px" }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 21 21"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g clipPath="url(#clip0_580_4010)">
        <path
          d="M4.04167 0.5H16.9583C18.9167 0.5 20.5 2.08333 20.5 4.04167V16.4583C20.5 18.4167 18.9167 20 16.9583 20H4.04167C2.08333 20 0.5 18.4167 0.5 16.4583V4.04167C0.5 2.08333 2.08333 0.5 4.04167 0.5Z"
          fill="#0052CC"
        />
        <path
          d="M10.5 5.5L7.5 12.5H10.5L9.5 15.5L13.5 8.5H10.5L10.5 5.5Z"
          fill="white"
        />
      </g>
      <defs>
        <clipPath id="clip0_580_4010">
          <rect x="0.5" y="0.5" width="20" height="19.5" fill="white" />
        </clipPath>
      </defs>
    </svg>
  );
}

// Setting default values for the props of Atlassian
// Removed defaultProps - using default parameters instead

// Typechecking props for the Atlassian
Atlassian.propTypes = {
  size: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
};

export default Atlassian;
