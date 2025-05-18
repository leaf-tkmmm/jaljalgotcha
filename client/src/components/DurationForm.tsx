import React, { useState, useEffect } from "react";
import {
  TextField,
  Button,
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
  // Hardcoded attempts to 1
  const [attempts] = useState("1");
  const [error, setError] = useState<string | null>(null);

  // Clear error when duration changes
  useEffect(() => {
    if (error) setError(null);
  }, [duration]);

  // Validate duration is a valid number and doesn't exceed 1000 minutes
  const validateDuration = (durationStr: string): boolean => {
    const minutes = Number(durationStr);
    return !isNaN(minutes) && minutes > 0 && minutes <= 1000;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!duration.trim()) {
      setError("時間を入力してください");
      return;
    }
    
    if (duration.includes(':')) {
      setError("HH:MM:SS形式は使用できません。分単位で入力してください");
      return;
    }
    
    if (!validateDuration(duration)) {
      setError("有効な数値を入力してください（最大1000分まで）");
      return;
    }

    onSubmit({
      duration,
      attempts: parseInt(attempts, 10)
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
        何分間耐久しますか
      </Typography>

      <form onSubmit={handleSubmit}>
        <Stack spacing={4}>
          <>
            <Box sx={{ mb: 1 }}>
              <TextField
                fullWidth
                label="合計時間(分)"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                required
                placeholder="例: 30"
                type="number"
                inputProps={{ min: 1, max: 1000 }}
                variant="outlined"
                error={!!error}
                helperText={error || "最大1000分"}
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
              {isLoading ? "検索中..." : "ガチャ"}
            </Button>
          </Box>
        </Stack>
      </form>
    </Paper>
  );
};

export default DurationForm;
