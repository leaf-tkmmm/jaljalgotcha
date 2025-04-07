import React, { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Alert,
  CssBaseline,
  ThemeProvider,
  createTheme,
} from "@mui/material";
import DurationForm from "./components/DurationForm";
import VideoList from "./components/VideoList";
import { GetCombinationsParams, getCombinations } from "./services/api";
import { VideoCombination } from "./types";

// MUIのテーマ設定
const theme = createTheme({
  palette: {
    primary: {
      main: "#3f51b5",
    },
    secondary: {
      main: "#f50057",
    },
  },
  typography: {
    fontFamily: [
      "Roboto",
      "Helvetica",
      "Arial",
      "sans-serif",
      "-apple-system",
      "BlinkMacSystemFont",
    ].join(","),
  },
});

function App() {
  const [combinations, setCombinations] = useState<VideoCombination[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (params: GetCombinationsParams) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await getCombinations(params);
      setCombinations(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "エラーが発生しました");
      setCombinations([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md" className="py-8">
        <Box className="mb-6">
          <Typography variant="h4" component="h1" className="mb-2 text-center">
            JalJalGotcha
          </Typography>
          <Typography
            variant="subtitle1"
            className="text-center text-gray-600 mb-6"
          >
            動画の時間組み合わせシステム
          </Typography>
        </Box>

        <DurationForm onSubmit={handleSubmit} isLoading={isLoading} />

        {error && (
          <Alert severity="error" className="mb-4">
            {error}
          </Alert>
        )}

        {!isLoading && combinations.length > 0 && (
          <VideoList combinations={combinations} />
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
