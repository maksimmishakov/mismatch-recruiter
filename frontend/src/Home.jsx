import React from 'react';
import { Container, Box, Typography, Paper, Grid } from '@mui/material';

const Home = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" gutterBottom>
          Welcome to MisMatch Recruiter
        </Typography>
        <Typography variant="subtitle1" color="textSecondary" paragraph>
          Intelligent job matching system powered by advanced analytics
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              About
            </Typography>
            <Typography paragraph>
              MisMatch Recruiter is a cutting-edge platform that leverages AI and machine learning
              to match candidates with job positions. Our advanced algorithms analyze skills,
              experience, and career goals to find the perfect match.
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Features
            </Typography>
            <Typography component="div">
              <ul>
                <li>Intelligent matching algorithm</li>
                <li>Real-time analytics and insights</li>
                <li>Comprehensive candidate profiling</li>
                <li>Advanced job position analysis</li>
                <li>Data-driven recommendations</li>
              </ul>
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      <Box sx={{ mt: 4 }}>
        <Paper sx={{ p: 3, backgroundColor: '#f5f5f5' }}>
          <Typography variant="h5" gutterBottom>
            Getting Started
          </Typography>
          <Typography paragraph>
            Navigate to the Analytics section to view detailed reports and insights about your matches.
            Use the menu to explore different features of the platform.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default Home;
