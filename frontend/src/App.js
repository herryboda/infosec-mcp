import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  CircularProgress,
  ThemeProvider,
  createTheme,
  CssBaseline,
  AppBar,
  Toolbar,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Menu as MenuIcon,
  QuestionAnswer as QuestionAnswerIcon,
  Upload as UploadIcon,
  Brightness4 as DarkModeIcon,
  Brightness7 as LightModeIcon,
} from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [documentContent, setDocumentContent] = useState('');
  const [documentName, setDocumentName] = useState('');

  const handleAskQuestion = async () => {
    if (!question.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/v1/ask', 
        { question },
        { headers: { 'X-API-Key': 'your_api_key' } }
      );
      setAnswer(response.data.answer);
    } catch (error) {
      setAnswer('Error: ' + error.message);
    }
    setLoading(false);
  };

  const handleUploadDocument = async () => {
    if (!documentContent.trim() || !documentName.trim()) return;
    
    setLoading(true);
    try {
      await axios.post('http://localhost:8000/api/v1/ingest',
        { content: documentContent, name: documentName },
        { headers: { 'X-API-Key': 'your_api_key' } }
      );
      setDocumentContent('');
      setDocumentName('');
      alert('Document uploaded successfully!');
    } catch (error) {
      alert('Error: ' + error.message);
    }
    setLoading(false);
  };

  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              onClick={() => setDrawerOpen(true)}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Company Policy Assistant
            </Typography>
            <IconButton color="inherit" onClick={toggleTheme}>
              {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
          </Toolbar>
        </AppBar>

        <Drawer
          anchor="left"
          open={drawerOpen}
          onClose={() => setDrawerOpen(false)}
        >
          <Box sx={{ width: 250 }}>
            <List>
              <ListItem button onClick={() => setDrawerOpen(false)}>
                <ListItemIcon>
                  <QuestionAnswerIcon />
                </ListItemIcon>
                <ListItemText primary="Ask Questions" />
              </ListItem>
              <ListItem button onClick={() => setDrawerOpen(false)}>
                <ListItemIcon>
                  <UploadIcon />
                </ListItemIcon>
                <ListItemText primary="Upload Policy" />
              </ListItem>
            </List>
            <Divider />
          </Box>
        </Drawer>

        <Container maxWidth="md" sx={{ mt: 4 }}>
          <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
            <Typography variant="h5" gutterBottom>
              Ask a Question
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={2}
              variant="outlined"
              placeholder="What would you like to know about company policies?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              sx={{ mb: 2 }}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={handleAskQuestion}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Ask'}
            </Button>
          </Paper>

          {answer && (
            <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
              <Typography variant="h5" gutterBottom>
                Answer
              </Typography>
              <Box sx={{ mt: 2 }}>
                <ReactMarkdown>{answer}</ReactMarkdown>
              </Box>
            </Paper>
          )}

          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Upload Policy Document
            </Typography>
            <TextField
              fullWidth
              label="Document Name"
              variant="outlined"
              value={documentName}
              onChange={(e) => setDocumentName(e.target.value)}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              multiline
              rows={6}
              variant="outlined"
              label="Document Content"
              value={documentContent}
              onChange={(e) => setDocumentContent(e.target.value)}
              sx={{ mb: 2 }}
            />
            <Button
              variant="contained"
              color="secondary"
              onClick={handleUploadDocument}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Upload'}
            </Button>
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App; 