import React from "react";
import { Typography, Paper, Box, Divider } from "@mui/material";
import VideoListItem from "./VideoListItem";
import { VideoCombination } from "../types";

interface VideoListProps {
  combinations: VideoCombination[];
}

const VideoList: React.FC<VideoListProps> = ({ combinations }) => {
  if (combinations.length === 0) {
    return (
      <Paper className="p-6 text-center">
        <Typography variant="subtitle1">
          条件に合う組み合わせが見つかりませんでした。
        </Typography>
      </Paper>
    );
  }

  return (
    <div>
      <Typography variant="h5" component="h2" className="mb-4">
        動画の組み合わせ ({combinations.length})
      </Typography>

      {combinations.map((combo, index) => (
        <Paper key={index} className="p-4 mb-6">
          <Box className="mb-3">
            <Typography variant="h6" className="mb-2">
              組み合わせ {index + 1}
            </Typography>
            <Divider />
          </Box>

          {combo.videos.map((video) => (
            <VideoListItem key={video.id} video={video} />
          ))}

          <Paper className="p-3 mt-4 bg-gray-50">
            <Box className="flex justify-between flex-wrap">
              <Typography variant="body1" className="mr-4">
                <strong>合計時間:</strong> {combo.total_time_formatted}
              </Typography>
              <Typography variant="body1">
                <strong>残り時間:</strong> {combo.remaining_time_formatted}
              </Typography>
            </Box>
          </Paper>
        </Paper>
      ))}
    </div>
  );
};

export default VideoList;
