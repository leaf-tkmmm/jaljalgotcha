import { useState, useRef, useMemo } from "react";
import {
  Container,
  Typography,
  Box,
  Alert,
  CssBaseline,
  ThemeProvider,
  createTheme,
  IconButton,
  Tooltip,
} from "@mui/material";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import DurationForm from "./components/DurationForm";
import VideoList from "./components/VideoList";
import VideoListSkeleton from "./components/VideoListSkeleton";
import { GetCombinationsParams, getCombinations } from "./services/api";
import { VideoCombination } from "./types";

// テーマ設定の作成関数
const createAppTheme = (mode: "light" | "dark") =>
  createTheme({
    palette: {
      mode,
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
        default: mode === "light" ? "#f9f9f9" : "#1f1f1f",
        paper: mode === "light" ? "#ffffff" : "#2c2c2c",
      },
      text: {
        primary: mode === "light" ? "#333333" : "#f5f5f5",
        secondary: mode === "light" ? "#666666" : "#b0b0b0",
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
  const [currentDuration, setCurrentDuration] = useState<string>("N");
  const videoListRef = useRef<HTMLDivElement>(null);
  const [mode, setMode] = useState<"light" | "dark">("light");

  // テーマの作成
  const theme = useMemo(() => createAppTheme(mode), [mode]);

  // テーマ切り替え関数
  const toggleColorMode = () => {
    setMode((prevMode) => (prevMode === "light" ? "dark" : "light"));
  };

  const handleSubmit = async (params: GetCombinationsParams) => {
    setIsLoading(true);
    setError(null);
    setCurrentDuration(params.duration);

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
        <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 2 }}>
          <Tooltip
            title={`${
              mode === "light" ? "ダークモード" : "ライトモード"
            }に切り替え`}
          >
            <IconButton onClick={toggleColorMode} color="inherit">
              {mode === "light" ? <Brightness4Icon /> : <Brightness7Icon />}
            </IconButton>
          </Tooltip>
        </Box>
        <Box sx={{ mb: 6 }}>
          <Typography
            variant="h3"
            component="h1"
            sx={{
              mb: 2,
              textAlign: "center",
              fontWeight: "bold",
              fontSize: { xs: "2rem", sm: "2.5rem", md: "3rem" },
            }}
          >
            ジャルジャルのガチャする奴
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
            <VideoList 
              ref={videoListRef} 
              combinations={combinations} 
              duration={currentDuration}
            />
          )
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
