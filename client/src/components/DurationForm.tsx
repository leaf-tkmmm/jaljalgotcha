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
    <Paper elevation={3} className="p-6 mb-6">
      <Typography variant="h5" component="h2" className="mb-4">
        動画の時間組み合わせ検索
      </Typography>

      <form onSubmit={handleSubmit}>
        <Stack spacing={3}>
          <div>
            <TextField
              fullWidth
              label="希望する時間（分単位または HH:MM:SS形式）"
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              required
              placeholder="例: 30 または 00:30:00"
            />
          </div>

          <div>
            <TextField
              fullWidth
              label="生成する組み合わせの数"
              type="number"
              value={attempts}
              onChange={(e) => setAttempts(e.target.value)}
              inputProps={{ min: 1, max: 10 }}
            />
          </div>

          <div>
            <FormControl component="fieldset">
              <Typography variant="subtitle1">データソース:</Typography>
              <RadioGroup
                row
                value={dataSource}
                onChange={(e) => setDataSource(e.target.value)}
              >
                <FormControlLabel
                  value="memory"
                  control={<Radio />}
                  label="メモリ内サンプルデータ"
                />
                <FormControlLabel
                  value="youtube"
                  control={<Radio />}
                  label="YouTube API"
                />
              </RadioGroup>
            </FormControl>
          </div>

          <div>
            <Box className="flex justify-end">
              <Button
                variant="contained"
                color="primary"
                type="submit"
                disabled={isLoading}
                className="bg-blue-600 hover:bg-blue-700"
              >
                {isLoading ? "検索中..." : "動画組み合わせを取得"}
              </Button>
            </Box>
          </div>
        </Stack>
      </form>
    </Paper>
  );
};

export default DurationForm;
