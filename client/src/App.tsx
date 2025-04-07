import { useState, useRef } from "react";
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
import VideoListSkeleton from "./components/VideoListSkeleton";
import { GetCombinationsParams, getCombinations } from "./services/api";
import { VideoCombination } from "./types";

// MUIのテーマ設定
const theme = createTheme({
  palette: {
    primary: {
      main: "#3f51b5",
      light: "#7986cb",
      dark: "#303f9f",
    },
    secondary: {
      main: "#f50057",
      light: "#ff4081",
      dark: "#c51162",
    },
    background: {
      default: "#f9f9f9",
      paper: "#ffffff",
    },
    text: {
      primary: "#333333",
      secondary: "#666666",
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
    h3: {
      fontWeight: 700,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiPaper: {
      defaultProps: {
        elevation: 0,
      },
      styleOverrides: {
        root: {
          boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          borderRadius: 8,
          fontWeight: 500,
        },
      },
    },
  },
});

function App() {
  const [combinations, setCombinations] = useState<VideoCombination[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const videoListRef = useRef<HTMLDivElement>(null);

  const handleSubmit = async (params: GetCombinationsParams) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await getCombinations(params);
      setCombinations(data);

      // 検索結果が表示されたら、少し遅延してスクロール
      if (data.length > 0) {
        setTimeout(() => {
          videoListRef.current?.scrollIntoView({ behavior: "smooth" });
        }, 100);
      }
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
      <Container maxWidth="md" sx={{ py: 6, px: { xs: 3, sm: 4 } }}>
        <Box sx={{ mb: 6 }}>
          <Typography
            variant="h3"
            component="h1"
            sx={{ mb: 2, textAlign: "center", fontWeight: "bold" }}
          >
            JalJalGotcha
          </Typography>
          <Typography
            variant="subtitle1"
            sx={{ textAlign: "center", color: "text.secondary", mb: 4 }}
          >
            動画の時間組み合わせシステム
          </Typography>
        </Box>

        <DurationForm onSubmit={handleSubmit} isLoading={isLoading} />

        {error && (
          <Alert
            severity="error"
            sx={{
              mb: 4,
              borderRadius: 2,
              "& .MuiAlert-icon": {
                fontSize: "1.25rem",
              },
            }}
          >
            {error}
          </Alert>
        )}

        {isLoading ? (
          <VideoListSkeleton count={3} />
        ) : (
          combinations.length > 0 && (
            <VideoList ref={videoListRef} combinations={combinations} />
          )
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
