import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import { CssBaseline } from '@mui/material';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import EqualizerIcon from '@mui/icons-material/Equalizer';

const drawerWidth = 240;

export default function Navbar({ onLogout }) {
  const location = useLocation();

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Tablero
          </Typography>
          <Button color="inherit" onClick={onLogout}>Cerrar Sesión</Button>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <ListItem key="1" disablePadding>
            <ListItemButton component={Link} to="/" selected={"/" === location.pathname}>
              <ListItemIcon><AutoGraphIcon /></ListItemIcon>
              <ListItemText primary="Estacionamiento" />
            </ListItemButton>
          </ListItem>
          <ListItem key="2" disablePadding>
            <ListItemButton component={Link} to="/pagina2" selected={"/pagina2" === location.pathname}>
              <ListItemIcon><EqualizerIcon /></ListItemIcon>
              <ListItemText primary="Historial" />
            </ListItemButton>
          </ListItem>
          <ListItem key="3" disablePadding>
            <ListItemButton component={Link} to="/pagina3" selected={"/pagina3" === location.pathname}>
              <ListItemIcon><EqualizerIcon /></ListItemIcon>
              <ListItemText primary="Reportes" />
            </ListItemButton>
          </ListItem>
        </Box>
      </Drawer>
    </Box>
  );
}
