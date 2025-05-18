import React from "react";
import { Paper, Typography, Box, Chip } from "@mui/material";
import { Video } from "../types";

interface VideoListItemProps {
  video: Video;
}

const VideoListItem: React.FC<VideoListItemProps> = ({ video }) => {
  const handleClick = () => {
    if (video.url) {
      window.open(video.url, "_blank", "noopener,noreferrer");
    }
  };

  return (
    <Paper
      onClick={handleClick}
      sx={{
        cursor: video.url ? "pointer" : "default",
        p: { xs: 2, sm: 3 },
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
          flexDirection: "column",
          alignItems: "flex-start",
        }}
      >
        {video.thumbnail_url && (
          <Box
            sx={{
              width: "100%",
              display: "flex",
              justifyContent: "center",
              mb: 1.5,
            }}
          >
            <Box
              component="img"
              src={video.thumbnail_url}
              alt={`${video.title}のサムネイル`}
              sx={{
                width: { xs: 160, sm: 240 },
                height: { xs: 90, sm: 135 },
                objectFit: "cover",
                borderRadius: 1,
                flexShrink: 0,
              }}
            />
          </Box>
        )}
        
        <Box
          sx={{
            width: "100%",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
          }}
        >
          <Typography
            variant="body2"
            sx={{
              fontWeight: "medium",
              color: "text.primary",
              overflow: "hidden",
              textOverflow: "ellipsis",
              fontSize: { xs: "0.85rem", sm: "0.95rem" },
              lineHeight: 1.4,
              display: "-webkit-box",
              WebkitLineClamp: 2,
              WebkitBoxOrient: "vertical",
              wordBreak: "break-word",
              maxWidth: "75%",
            }}
          >
            {video.title}
          </Typography>
          
          <Chip
            label={video.duration_formatted}
            color="primary"
            size="small"
            sx={{
              fontWeight: "bold",
              minWidth: "70px",
              textAlign: "center",
              borderRadius: "16px",
              fontSize: { xs: "0.7rem", sm: "0.75rem" },
              height: { xs: "24px", sm: "28px" },
              ml: 1,
            }}
          />
        </Box>
      </Box>
    </Paper>
  );
};

export default VideoListItem;
