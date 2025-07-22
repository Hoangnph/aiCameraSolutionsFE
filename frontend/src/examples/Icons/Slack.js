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

function Slack({ size = "16px" }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 21 21"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g clipPath="url(#clip0_580_4011)">
        <path
          d="M4.04167 0.5H16.9583C18.9167 0.5 20.5 2.08333 20.5 4.04167V16.4583C20.5 18.4167 18.9167 20 16.9583 20H4.04167C2.08333 20 0.5 18.4167 0.5 16.4583V4.04167C0.5 2.08333 2.08333 0.5 4.04167 0.5Z"
          fill="#E01E5A"
        />
        <path
          d="M8.5 6.5C8.5 7.32843 7.82843 8 7 8C6.17157 8 5.5 7.32843 5.5 6.5C5.5 5.67157 6.17157 5 7 5C7.82843 5 8.5 5.67157 8.5 6.5Z"
          fill="white"
        />
        <path
          d="M15.5 6.5C15.5 7.32843 14.8284 8 14 8C13.1716 8 12.5 7.32843 12.5 6.5C12.5 5.67157 13.1716 5 14 5C14.8284 5 15.5 5.67157 15.5 6.5Z"
          fill="white"
        />
        <path
          d="M8.5 14.5C8.5 15.3284 7.82843 16 7 16C6.17157 16 5.5 15.3284 5.5 14.5C5.5 13.6716 6.17157 13 7 13C7.82843 13 8.5 13.6716 8.5 14.5Z"
          fill="white"
        />
        <path
          d="M15.5 14.5C15.5 15.3284 14.8284 16 14 16C13.1716 16 12.5 15.3284 12.5 14.5C12.5 13.6716 13.1716 13 14 13C14.8284 13 15.5 13.6716 15.5 14.5Z"
          fill="white"
        />
      </g>
      <defs>
        <clipPath id="clip0_580_4011">
          <rect x="0.5" y="0.5" width="20" height="19.5" fill="white" />
        </clipPath>
      </defs>
    </svg>
  );
}

// Setting default values for the props of Slack
// Removed defaultProps - using default parameters instead

// Typechecking props for the Slack
Slack.propTypes = {
  size: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
};

export default Slack;
