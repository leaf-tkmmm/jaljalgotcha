import React from "react";
import { Paper, Typography, Box, Chip } from "@mui/material";
import { Video } from "../types";

interface VideoListItemProps {
  video: Video;
}

const VideoListItem: React.FC<VideoListItemProps> = ({ video }) => {
  return (
    <Paper className="p-4 mb-2 hover:shadow-md transition-shadow">
      <Box className="flex justify-between items-center">
        <Typography variant="h6" className="font-medium text-gray-800 truncate">
          {video.title}
        </Typography>
        <Chip
          label={video.duration_formatted}
          color="primary"
          size="small"
          className="ml-2 min-w-[80px] text-center"
        />
      </Box>
      {video.url && (
        <Typography variant="body2" className="text-blue-600 mt-1 truncate">
          <a href={video.url} target="_blank" rel="noopener noreferrer">
            {video.url}
          </a>
        </Typography>
      )}
    </Paper>
  );
};

export default VideoListItem;
