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
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: { xs: "wrap", sm: "nowrap" },
        }}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            flexGrow: 1,
            mr: 2,
            overflow: "hidden",
          }}
        >
          {video.thumbnail_url && (
            <Box
              component="img"
              src={video.thumbnail_url}
              alt={`${video.title}のサムネイル`}
              sx={{
                width: { xs: 80, sm: 120 },
                height: { xs: 45, sm: 68 },
                objectFit: "cover",
                borderRadius: 1,
                mr: 2,
                flexShrink: 0,
              }}
            />
          )}
          <Typography
            variant="h6"
            sx={{
              fontWeight: "medium",
              color: "text.primary",
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: { xs: "normal", sm: "nowrap" },
              maxWidth: { xs: "100%", sm: "100%" },
              mb: { xs: 1, sm: 0 },
              fontSize: { xs: "0.95rem", sm: "1.125rem" },
              lineHeight: { xs: 1.4, sm: 1.6 },
              display: "-webkit-box",
              WebkitLineClamp: { xs: 3, sm: 1 },
              WebkitBoxOrient: "vertical",
              wordBreak: "break-word",
            }}
          >
            {video.title}
          </Typography>
        </Box>
        <Chip
          label={video.duration_formatted}
          color="primary"
          size="medium"
          sx={{
            fontWeight: "bold",
            minWidth: "85px",
            textAlign: "center",
            borderRadius: "16px",
            fontSize: { xs: "0.75rem", sm: "0.875rem" },
            height: { xs: "28px", sm: "32px" },
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
            whiteSpace: { xs: "normal", sm: "normal" },
            fontSize: { xs: "0.75rem", sm: "0.875rem" },
            wordBreak: "break-all",
            display: "-webkit-box",
            WebkitLineClamp: { xs: 2, sm: 2 },
            WebkitBoxOrient: "vertical",
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
