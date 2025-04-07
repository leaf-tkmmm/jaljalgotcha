import React, { useState } from "react";
import {
  TextField,
  Button,
  FormControl,
  FormControlLabel,
  Radio,
  RadioGroup,
  Typography,
  Paper,
  Box,
  Stack,
} from "@mui/material";
import { GetCombinationsParams } from "../services/api";

interface DurationFormProps {
  onSubmit: (params: GetCombinationsParams) => void;
  isLoading: boolean;
}

const DurationForm: React.FC<DurationFormProps> = ({ onSubmit, isLoading }) => {
  const [duration, setDuration] = useState("");
  const [attempts, setAttempts] = useState("3");
  const [dataSource, setDataSource] = useState("memory");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    onSubmit({
      duration,
      attempts: parseInt(attempts, 10),
      useYoutube: dataSource === "youtube",
    });
  };

  return (
    <Paper
      elevation={3}
      sx={{
        p: { xs: 3, sm: 4, md: 5 },
        mb: 4,
        borderRadius: 2,
        boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
      }}
    >
      <Typography
        variant="h5"
        component="h2"
        sx={{
          mb: { xs: 3, sm: 4 },
          fontWeight: "medium",
          color: "primary.main",
          fontSize: { xs: "1.25rem", sm: "1.5rem" },
        }}
      >
        動画の時間組み合わせ検索
      </Typography>

      <form onSubmit={handleSubmit}>
        <Stack spacing={4}>
          <>
            <Box sx={{ mb: 1 }}>
              <TextField
                fullWidth
                label="希望する時間（分単位または HH:MM:SS形式）"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                required
                placeholder="例: 30 または 00:30:00"
                variant="outlined"
                sx={{
                  "& .MuiOutlinedInput-root": {
                    borderRadius: 1.5,
                    "&:hover fieldset": {
                      borderColor: "primary.light",
                    },
                  },
                }}
              />
            </Box>

            <Box sx={{ mb: 1 }}>
              <TextField
                fullWidth
                label="生成する組み合わせの数"
                type="number"
                value={attempts}
                onChange={(e) => setAttempts(e.target.value)}
                inputProps={{ min: 1, max: 10 }}
                variant="outlined"
                sx={{
                  "& .MuiOutlinedInput-root": {
                    borderRadius: 1.5,
                  },
                }}
              />
            </Box>

            <Box sx={{ mb: 2 }}>
              <FormControl component="fieldset" sx={{ width: "100%", mt: 1 }}>
                <Typography
                  variant="subtitle1"
                  sx={{ mb: 1, fontWeight: "medium" }}
                >
                  データソース:
                </Typography>
                <RadioGroup
                  row
                  value={dataSource}
                  onChange={(e) => setDataSource(e.target.value)}
                  sx={{
                    justifyContent: { xs: "flex-start", sm: "space-around" },
                    flexDirection: { xs: "column", sm: "row" },
                  }}
                >
                  <FormControlLabel
                    value="memory"
                    control={<Radio color="primary" />}
                    label="メモリ内サンプルデータ"
                    sx={{ mr: 4, mb: { xs: 1, sm: 0 } }}
                  />
                  <FormControlLabel
                    value="youtube"
                    control={<Radio color="primary" />}
                    label="YouTube API"
                  />
                </RadioGroup>
              </FormControl>
            </Box>
          </>

          <Box
            sx={{
              display: "flex",
              justifyContent: { xs: "center", sm: "flex-end" },
              mt: 2,
            }}
          >
            <Button
              variant="contained"
              color="primary"
              type="submit"
              disabled={isLoading}
              size="large"
              sx={{
                px: { xs: 3, sm: 4 },
                py: 1,
                borderRadius: 2,
                boxShadow: 3,
                fontSize: { xs: "0.875rem", sm: "1rem" },
                width: { xs: "100%", sm: "auto" },
                "&:hover": {
                  boxShadow: 4,
                },
              }}
            >
              {isLoading ? "検索中..." : "動画組み合わせを取得"}
            </Button>
          </Box>
        </Stack>
      </form>
    </Paper>
  );
};

export default DurationForm;
