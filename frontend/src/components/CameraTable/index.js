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
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Chip from "@mui/material/Chip";
import ButtonGroup from "@mui/material/ButtonGroup";
import Tooltip from "@mui/material/Tooltip";

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";

// React icons
import { IoCamera } from "react-icons/io5";
import { IoEye } from "react-icons/io5";
import { IoPencil } from "react-icons/io5";
import { IoTrash } from "react-icons/io5";
import { IoPlay } from "react-icons/io5";
import { IoStop } from "react-icons/io5";
import { IoLocation } from "react-icons/io5";
import { IoTime } from "react-icons/io5";
import { IoWifi } from "react-icons/io5";
import { IoClose } from "react-icons/io5";

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

function CameraTable({ cameras, loading, onStatusChange, onEdit, onDelete }) {
  const history = useHistory();

  const tableStyles = {
    container: {
      background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
      backdropFilter: 'blur(10px)',
      WebkitBackdropFilter: 'blur(10px)',
      border: '1px solid rgba(255,255,255,0.2)',
      borderRadius: '20px',
      overflow: 'hidden',
      boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
      position: 'relative',
      '&::before': {
        content: '""',
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.05) 100%)',
        borderRadius: '20px',
        zIndex: -1
      },
      '& .MuiTable-root': {
        backgroundColor: 'transparent !important',
        display: 'table !important',
        width: '100% !important',
        tableLayout: 'fixed !important'
      },
      '& .MuiTableHead-root': {
        background: 'linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%)',
        backdropFilter: 'blur(10px)',
        WebkitBackdropFilter: 'blur(10px)',
        display: 'table-header-group !important'
      },
      '& .MuiTableBody-root': {
        backgroundColor: 'transparent !important',
        display: 'table-row-group !important'
      },
      '& .MuiTableRow-root': {
        backgroundColor: 'transparent !important',
        display: 'table-row !important',
        transition: 'all 0.3s ease',
        '&:hover': {
          background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%) !important',
          backdropFilter: 'blur(5px)',
          WebkitBackdropFilter: 'blur(5px)',
          transform: 'translateY(-2px)',
          boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
        }
      },
      '& .MuiTableCell-root': {
        backgroundColor: 'transparent !important',
        borderColor: 'rgba(255,255,255,0.1)',
        color: 'white',
        position: 'relative',
        display: 'table-cell !important',
        verticalAlign: 'middle !important'
      }
    },
    table: {
      minWidth: 650,
      backgroundColor: 'transparent !important',
      tableLayout: 'fixed',
      width: '100%',
      '& .MuiTable-root': {
        backgroundColor: 'transparent !important'
      },
      '& .MuiTableHead-root': {
        backgroundColor: 'transparent !important'
      },
      '& .MuiTableBody-root': {
        backgroundColor: 'transparent !important'
      }
    },
    headerCell: {
      color: 'white',
      fontWeight: '700',
      fontSize: '14px',
      padding: '20px 16px',
      background: 'linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%)',
      backdropFilter: 'blur(10px)',
      WebkitBackdropFilter: 'blur(10px)',
      borderBottom: '2px solid rgba(255,255,255,0.2)',
      textAlign: 'center',
      minHeight: '56px',
      position: 'relative',
      display: 'table-cell',
      verticalAlign: 'middle',
      '&::after': {
        content: '""',
        position: 'absolute',
        bottom: 0,
        left: '50%',
        transform: 'translateX(-50%)',
        width: '0%',
        height: '2px',
        background: 'linear-gradient(90deg, #0075FF, #00D4FF)',
        transition: 'width 0.3s ease'
      },
      '&:hover::after': {
        width: '80%'
      }
    },
    headerCellCenter: {
      color: 'white',
      fontWeight: '700',
      fontSize: '14px',
      padding: '20px 16px',
      background: 'linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%)',
      backdropFilter: 'blur(10px)',
      WebkitBackdropFilter: 'blur(10px)',
      borderBottom: '2px solid rgba(255,255,255,0.2)',
      textAlign: 'center',
      minHeight: '56px',
      position: 'relative',
      display: 'table-cell',
      verticalAlign: 'middle',
      '&::after': {
        content: '""',
        position: 'absolute',
        bottom: 0,
        left: '50%',
        transform: 'translateX(-50%)',
        width: '0%',
        height: '2px',
        background: 'linear-gradient(90deg, #0075FF, #00D4FF)',
        transition: 'width 0.3s ease'
      },
      '&:hover::after': {
        width: '80%'
      }
    },
    dataCell: {
      borderBottom: '1px solid rgba(255,255,255,0.08)',
      color: 'white',
      padding: '20px 16px',
      backgroundColor: 'transparent !important',
      textAlign: 'left',
      minHeight: '56px',
      maxWidth: '200px',
      position: 'relative',
      transition: 'all 0.3s ease',
      display: 'table-cell',
      verticalAlign: 'middle',
      '&::before': {
        content: '""',
        position: 'absolute',
        left: 0,
        top: 0,
        bottom: 0,
        width: '3px',
        background: 'linear-gradient(180deg, transparent, rgba(255,255,255,0.1), transparent)',
        opacity: 0,
        transition: 'opacity 0.3s ease'
      },
      '&:hover::before': {
        opacity: 1
      }
    },
    dataCellCenter: {
      borderBottom: '1px solid rgba(255,255,255,0.08)',
      color: 'white',
      padding: '20px 16px',
      backgroundColor: 'transparent !important',
      textAlign: 'center',
      minHeight: '56px',
      maxWidth: '200px',
      position: 'relative',
      transition: 'all 0.3s ease',
      display: 'table-cell',
      verticalAlign: 'middle',
      '&::before': {
        content: '""',
        position: 'absolute',
        left: 0,
        top: 0,
        bottom: 0,
        width: '3px',
        background: 'linear-gradient(180deg, transparent, rgba(255,255,255,0.1), transparent)',
        opacity: 0,
        transition: 'opacity 0.3s ease'
      },
      '&:hover::before': {
        opacity: 1
      }
    },
    truncatedText: {
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap',
      maxWidth: '100%',
      display: 'block'
    },
    longTextCell: {
      maxWidth: '250px',
      '& .truncated-text': {
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap',
        maxWidth: '100%',
        display: 'block'
      }
    },
    emptyCell: {
      border: 'none',
      py: 8,
      backgroundColor: 'transparent !important',
      textAlign: 'center'
    }
  };

  if (loading) {
    return (
      <TableContainer sx={tableStyles.container}>
        <Table sx={tableStyles.table}>
          <TableBody>
            <TableRow>
              <TableCell colSpan={7} sx={tableStyles.emptyCell}>
                <VuiBox display="flex" justifyContent="center" alignItems="center">
                  <VuiBox textAlign="center">
                    <VuiBox
                      bgColor="info"
                      color="white"
                      width="4rem"
                      height="4rem"
                      borderRadius="lg"
                      display="flex"
                      justifyContent="center"
                      alignItems="center"
                      margin="0 auto"
                      mb={2}
                    >
                      <IoCamera size="24px" />
                    </VuiBox>
                    <VuiTypography variant="h6" color="white" fontWeight="medium">
                      Loading cameras...
                    </VuiTypography>
                  </VuiBox>
                </VuiBox>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    );
  }

  if (cameras.length === 0) {
    return (
      <TableContainer sx={tableStyles.container}>
        <Table sx={tableStyles.table}>
          <TableBody>
            <TableRow>
              <TableCell colSpan={7} sx={tableStyles.emptyCell}>
                <VuiBox display="flex" justifyContent="center" alignItems="center">
                  <VuiBox textAlign="center">
                    <VuiBox
                      bgColor="grey-600"
                      color="white"
                      width="4rem"
                      height="4rem"
                      borderRadius="lg"
                      display="flex"
                      justifyContent="center"
                      alignItems="center"
                      margin="0 auto"
                      mb={2}
                    >
                      <IoCamera size="24px" />
                    </VuiBox>
                    <VuiTypography variant="h6" color="white" fontWeight="medium" mb={1}>
                      No cameras found
                    </VuiTypography>
                    <VuiTypography variant="button" color="text" opacity={0.7}>
                      Add your first camera to get started
                    </VuiTypography>
                  </VuiBox>
                </VuiBox>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    );
  }

  return (
    <TableContainer sx={tableStyles.container}>
      <Table sx={tableStyles.table} aria-label="cameras table">
        <TableHead>
          <TableRow>
            <TableCell sx={tableStyles.headerCellCenter}>
              <VuiTypography variant="button" color="white" fontWeight="bold">
                Camera
              </VuiTypography>
            </TableCell>
            <TableCell sx={tableStyles.headerCellCenter}>
              <VuiTypography variant="button" color="white" fontWeight="bold">
                IP Address
              </VuiTypography>
            </TableCell>
            <TableCell sx={tableStyles.headerCellCenter}>
              <VuiTypography variant="button" color="white" fontWeight="bold">
                RTSP URL
              </VuiTypography>
            </TableCell>
            <TableCell sx={tableStyles.headerCellCenter}>
              <VuiTypography variant="button" color="white" fontWeight="bold">
                Status
              </VuiTypography>
            </TableCell>
            <TableCell sx={tableStyles.headerCellCenter}>
              <VuiTypography variant="button" color="white" fontWeight="bold">
                Created
              </VuiTypography>
            </TableCell>
            <TableCell sx={tableStyles.headerCellCenter}>
              <VuiTypography variant="button" color="white" fontWeight="bold">
                Status Actions
              </VuiTypography>
            </TableCell>
            <TableCell sx={tableStyles.headerCellCenter}>
              <VuiTypography variant="button" color="white" fontWeight="bold">
                Actions
              </VuiTypography>
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {cameras.map((camera) => {
            const statusConfig = getStatusConfig(camera.status);
            return (
              <TableRow key={camera.id}>
                {/* Camera Name */}
                <TableCell sx={{...tableStyles.dataCell, maxWidth: '200px'}}>
                  <VuiBox display="flex" alignItems="center" width="100%">
                    <VuiBox
                      bgColor={statusConfig.bgColor}
                      color="white"
                      width="2.5rem"
                      height="2.5rem"
                      borderRadius="lg"
                      display="flex"
                      justifyContent="center"
                      alignItems="center"
                      mr={2}
                      shadow="md"
                      flexShrink={0}
                    >
                      <IoCamera size="16px" />
                    </VuiBox>
                    <Tooltip 
                      title={camera.name} 
                      placement="top"
                      arrow
                      sx={{
                        '& .MuiTooltip-tooltip': {
                          backgroundColor: 'rgba(0,0,0,0.9)',
                          color: 'white',
                          fontSize: '12px',
                          padding: '8px 12px',
                          borderRadius: '8px',
                          backdropFilter: 'blur(10px)',
                          border: '1px solid rgba(255,255,255,0.1)'
                        }
                      }}
                    >
                      <VuiTypography 
                        variant="button" 
                        color="white" 
                        fontWeight="bold"
                        sx={{
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                          maxWidth: '120px',
                          cursor: 'pointer'
                        }}
                      >
                        {camera.name}
                      </VuiTypography>
                    </Tooltip>
                  </VuiBox>
                </TableCell>

                {/* IP Address */}
                <TableCell sx={{...tableStyles.dataCell, maxWidth: '180px'}}>
                  <VuiBox display="flex" alignItems="center" width="100%">
                    <VuiBox
                      bgColor="grey-600"
                      color="white"
                      width="1.5rem"
                      height="1.5rem"
                      borderRadius="sm"
                      display="flex"
                      justifyContent="center"
                      alignItems="center"
                      mr={1}
                      flexShrink={0}
                    >
                      <IoWifi size="12px" />
                    </VuiBox>
                    <Tooltip 
                      title={camera.ip_address || 'Not configured'} 
                      placement="top"
                      arrow
                      sx={{
                        '& .MuiTooltip-tooltip': {
                          backgroundColor: 'rgba(0,0,0,0.9)',
                          color: 'white',
                          fontSize: '12px',
                          padding: '8px 12px',
                          borderRadius: '8px',
                          backdropFilter: 'blur(10px)',
                          border: '1px solid rgba(255,255,255,0.1)'
                        }
                      }}
                    >
                      <VuiTypography 
                        variant="button" 
                        color="white" 
                        fontWeight="medium"
                        sx={{
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                          maxWidth: '100px',
                          cursor: 'pointer'
                        }}
                      >
                        {camera.ip_address || 'Not configured'}
                      </VuiTypography>
                    </Tooltip>
                  </VuiBox>
                </TableCell>

                {/* RTSP URL */}
                <TableCell sx={{...tableStyles.dataCell, maxWidth: '250px'}}>
                  <VuiBox display="flex" alignItems="center" width="100%">
                    <VuiBox
                      bgColor="grey-600"
                      color="white"
                      width="1.5rem"
                      height="1.5rem"
                      borderRadius="sm"
                      display="flex"
                      justifyContent="center"
                      alignItems="center"
                      mr={1}
                      flexShrink={0}
                    >
                      <IoLocation size="12px" />
                    </VuiBox>
                    <Tooltip 
                      title={camera.rtsp_url || 'Not configured'} 
                      placement="top"
                      arrow
                      sx={{
                        '& .MuiTooltip-tooltip': {
                          backgroundColor: 'rgba(0,0,0,0.9)',
                          color: 'white',
                          fontSize: '12px',
                          padding: '8px 12px',
                          borderRadius: '8px',
                          backdropFilter: 'blur(10px)',
                          border: '1px solid rgba(255,255,255,0.1)',
                          maxWidth: '300px',
                          wordBreak: 'break-all'
                        }
                      }}
                    >
                      <VuiTypography 
                        variant="button" 
                        color="white" 
                        fontWeight="medium"
                        sx={{
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                          maxWidth: '180px',
                          cursor: 'pointer'
                        }}
                      >
                        {camera.rtsp_url || 'Not configured'}
                      </VuiTypography>
                    </Tooltip>
                  </VuiBox>
                </TableCell>

                {/* Status */}
                <TableCell sx={tableStyles.dataCell}>
                  <VuiBox display="flex" alignItems="center" width="100%">
                    <Chip
                      icon={statusConfig.icon}
                      label={camera.status}
                      color={statusConfig.color}
                      size="small"
                      sx={{
                        background: `linear-gradient(135deg, ${statusConfig.bgColor}20 0%, ${statusConfig.bgColor}10 100%)`,
                        backdropFilter: 'blur(10px)',
                        WebkitBackdropFilter: 'blur(10px)',
                        color: 'white',
                        fontWeight: '600',
                        textTransform: 'capitalize',
                        border: `1px solid ${statusConfig.bgColor}40`,
                        borderRadius: '12px',
                        padding: '4px 8px',
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          transform: 'translateY(-1px)',
                          boxShadow: `0 4px 12px ${statusConfig.bgColor}30`,
                          background: `linear-gradient(135deg, ${statusConfig.bgColor}30 0%, ${statusConfig.bgColor}20 100%)`
                        },
                        '& .MuiChip-icon': {
                          color: 'white',
                          fontSize: '16px'
                        },
                        '& .MuiChip-label': {
                          fontSize: '12px',
                          fontWeight: '600'
                        }
                      }}
                    />
                  </VuiBox>
                </TableCell>

                {/* Created Date */}
                <TableCell sx={tableStyles.dataCell}>
                  <VuiBox display="flex" alignItems="center" width="100%">
                    <VuiBox
                      bgColor="grey-600"
                      color="white"
                      width="1.5rem"
                      height="1.5rem"
                      borderRadius="sm"
                      display="flex"
                      justifyContent="center"
                      alignItems="center"
                      mr={1}
                      flexShrink={0}
                    >
                      <IoTime size="12px" />
                    </VuiBox>
                    <VuiTypography variant="button" color="white" fontWeight="medium">
                      {new Date(camera.created_at).toLocaleDateString()}
                    </VuiTypography>
                  </VuiBox>
                </TableCell>

                {/* Status Actions */}
                <TableCell sx={tableStyles.dataCellCenter}>
                  <ButtonGroup 
                    variant="outlined" 
                    size="small"
                    sx={{
                      background: 'rgba(255,255,255,0.05)',
                      backdropFilter: 'blur(10px)',
                      WebkitBackdropFilter: 'blur(10px)',
                      borderRadius: '12px',
                      padding: '4px',
                      border: '1px solid rgba(255,255,255,0.1)',
                      '& .MuiButton-root': {
                        borderColor: 'transparent',
                        color: 'white',
                        fontSize: '11px',
                        padding: '6px 12px',
                        minWidth: 'auto',
                        backgroundColor: 'transparent',
                        borderRadius: '8px',
                        transition: 'all 0.3s ease',
                        textTransform: 'none',
                        fontWeight: '500',
                        '&:hover': {
                          background: 'linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%)',
                          backdropFilter: 'blur(10px)',
                          WebkitBackdropFilter: 'blur(10px)',
                          transform: 'translateY(-1px)',
                          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
                        }
                      }
                    }}
                  >
                    {camera.status !== 'active' && (
                      <Button
                        onClick={() => onStatusChange(camera.id, 'active')}
                        sx={{ 
                          background: 'linear-gradient(135deg, rgba(76, 175, 80, 0.2) 0%, rgba(76, 175, 80, 0.1) 100%)',
                          color: '#4CAF50',
                          border: '1px solid rgba(76, 175, 80, 0.3)',
                          '&:hover': {
                            background: 'linear-gradient(135deg, rgba(76, 175, 80, 0.3) 0%, rgba(76, 175, 80, 0.2) 100%)',
                            borderColor: 'rgba(76, 175, 80, 0.5)',
                            color: '#4CAF50'
                          }
                        }}
                      >
                        <IoPlay size="12px" style={{ marginRight: '4px' }} />
                        Active
                      </Button>
                    )}
                    {camera.status !== 'offline' && (
                      <Button
                        onClick={() => onStatusChange(camera.id, 'offline')}
                        sx={{ 
                          background: 'linear-gradient(135deg, rgba(244, 67, 54, 0.2) 0%, rgba(244, 67, 54, 0.1) 100%)',
                          color: '#F44336',
                          border: '1px solid rgba(244, 67, 54, 0.3)',
                          '&:hover': {
                            background: 'linear-gradient(135deg, rgba(244, 67, 54, 0.3) 0%, rgba(244, 67, 54, 0.2) 100%)',
                            borderColor: 'rgba(244, 67, 54, 0.5)',
                            color: '#F44336'
                          }
                        }}
                      >
                        <IoStop size="12px" style={{ marginRight: '4px' }} />
                        Offline
                      </Button>
                    )}
                    {camera.status !== 'maintenance' && (
                      <Button
                        onClick={() => onStatusChange(camera.id, 'maintenance')}
                        sx={{ 
                          background: 'linear-gradient(135deg, rgba(255, 152, 0, 0.2) 0%, rgba(255, 152, 0, 0.1) 100%)',
                          color: '#FF9800',
                          border: '1px solid rgba(255, 152, 0, 0.3)',
                          '&:hover': {
                            background: 'linear-gradient(135deg, rgba(255, 152, 0, 0.3) 0%, rgba(255, 152, 0, 0.2) 100%)',
                            borderColor: 'rgba(255, 152, 0, 0.5)',
                            color: '#FF9800'
                          }
                        }}
                      >
                        <IoPencil size="12px" style={{ marginRight: '4px' }} />
                        Maint
                      </Button>
                    )}
                  </ButtonGroup>
                </TableCell>

                {/* Actions */}
                <TableCell sx={tableStyles.dataCellCenter}>
                  <ButtonGroup 
                    variant="outlined" 
                    size="small"
                    sx={{
                      background: 'rgba(255,255,255,0.05)',
                      backdropFilter: 'blur(10px)',
                      WebkitBackdropFilter: 'blur(10px)',
                      borderRadius: '12px',
                      padding: '4px',
                      border: '1px solid rgba(255,255,255,0.1)',
                      '& .MuiButton-root': {
                        borderColor: 'transparent',
                        color: 'white',
                        fontSize: '11px',
                        padding: '6px 12px',
                        minWidth: 'auto',
                        backgroundColor: 'transparent',
                        borderRadius: '8px',
                        transition: 'all 0.3s ease',
                        textTransform: 'none',
                        fontWeight: '500',
                        '&:hover': {
                          background: 'linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%)',
                          backdropFilter: 'blur(10px)',
                          WebkitBackdropFilter: 'blur(10px)',
                          transform: 'translateY(-1px)',
                          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
                        }
                      }
                    }}
                  >
                    <Button
                      onClick={() => history.push(`/cameras/${camera.id}`)}
                      sx={{ 
                        background: 'linear-gradient(135deg, rgba(33, 150, 243, 0.2) 0%, rgba(33, 150, 243, 0.1) 100%)',
                        color: '#2196F3',
                        border: '1px solid rgba(33, 150, 243, 0.3)',
                        '&:hover': {
                          background: 'linear-gradient(135deg, rgba(33, 150, 243, 0.3) 0%, rgba(33, 150, 243, 0.2) 100%)',
                          borderColor: 'rgba(33, 150, 243, 0.5)',
                          color: '#2196F3'
                        }
                      }}
                    >
                      <IoEye size="12px" style={{ marginRight: '4px' }} />
                      View
                    </Button>
                    <Button
                      onClick={() => onEdit(camera)}
                      sx={{ 
                        background: 'linear-gradient(135deg, rgba(255, 152, 0, 0.2) 0%, rgba(255, 152, 0, 0.1) 100%)',
                        color: '#FF9800',
                        border: '1px solid rgba(255, 152, 0, 0.3)',
                        '&:hover': {
                          background: 'linear-gradient(135deg, rgba(255, 152, 0, 0.3) 0%, rgba(255, 152, 0, 0.2) 100%)',
                          borderColor: 'rgba(255, 152, 0, 0.5)',
                          color: '#FF9800'
                        }
                      }}
                    >
                      <IoPencil size="12px" style={{ marginRight: '4px' }} />
                      Edit
                    </Button>
                    <Button
                      onClick={() => onDelete(camera)}
                      sx={{ 
                        background: 'linear-gradient(135deg, rgba(244, 67, 54, 0.2) 0%, rgba(244, 67, 54, 0.1) 100%)',
                        color: '#F44336',
                        border: '1px solid rgba(244, 67, 54, 0.3)',
                        '&:hover': {
                          background: 'linear-gradient(135deg, rgba(244, 67, 54, 0.3) 0%, rgba(244, 67, 54, 0.2) 100%)',
                          borderColor: 'rgba(244, 67, 54, 0.5)',
                          color: '#F44336'
                        }
                      }}
                    >
                      <IoClose size="12px" style={{ marginRight: '4px' }} />
                      Delete
                    </Button>
                  </ButtonGroup>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default CameraTable; 