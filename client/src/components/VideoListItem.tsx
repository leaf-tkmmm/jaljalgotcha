import React from "react";
import { Paper, Typography, Box, Chip } from "@mui/material";
import { Video } from "../types";

interface VideoListItemProps {
  video: Video;
}

const VideoListItem: React.FC<VideoListItemProps> = ({ video }) => {
  return (
    <Paper
      sx={{
        p: 3,
        mb: 2,
        borderRadius: 2,
        transition: "all 0.2s ease-in-out",
        boxShadow: "0 2px 10px rgba(0,0,0,0.05)",
        "&:hover": {
          boxShadow: "0 4px 15px rgba(0,0,0,0.1)",
          bgcolor: "rgba(0, 0, 0, 0.01)",
          transform: "translateY(-1px)",
        },
      }}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: { xs: "wrap", sm: "nowrap" },
        }}
      >
        <Typography
          variant="h6"
          sx={{
            fontWeight: "medium",
            color: "text.primary",
            mr: 2,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
            maxWidth: { xs: "100%", sm: "70%" },
            mb: { xs: 1, sm: 0 },
          }}
        >
          {video.title}
        </Typography>
        <Chip
          label={video.duration_formatted}
          color="primary"
          size="medium"
          sx={{
            fontWeight: "bold",
            minWidth: "90px",
            textAlign: "center",
            borderRadius: "16px",
          }}
        />
      </Box>
      {video.url && (
        <Typography
          variant="body2"
          sx={{
            color: "primary.main",
            mt: 1.5,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          <a
            href={video.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              textDecoration: "none",
              color: "inherit",
            }}
            className="hover:underline"
          >
            {video.url}
          </a>
        </Typography>
      )}
    </Paper>
  );
};

export default VideoListItem;
