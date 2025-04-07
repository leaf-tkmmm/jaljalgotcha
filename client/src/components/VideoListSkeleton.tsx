import React from "react";
import { Box, Paper, Skeleton, Divider } from "@mui/material";

interface VideoListSkeletonProps {
  count?: number;
}

const VideoItemSkeleton: React.FC = () => {
  return (
    <Paper
      sx={{
        p: 3,
        mb: 2,
        borderRadius: 2,
        boxShadow: "0 2px 10px rgba(0,0,0,0.05)",
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
        <Skeleton
          variant="text"
          sx={{
            width: { xs: "100%", sm: "70%" },
            height: 32,
            mb: { xs: 1, sm: 0 },
          }}
        />
        <Skeleton
          variant="rounded"
          width={90}
          height={32}
          sx={{ borderRadius: "16px" }}
        />
      </Box>
      <Skeleton variant="text" sx={{ width: "100%", height: 24, mt: 1.5 }} />
    </Paper>
  );
};

const CombinationSkeleton: React.FC = () => {
  return (
    <Paper
      sx={{
        p: { xs: 3, sm: 4 },
        mb: 4,
        borderRadius: 2,
        boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
      }}
    >
      <Box sx={{ mb: 3 }}>
        <Skeleton variant="text" sx={{ width: "30%", height: 32, mb: 2 }} />
        <Divider sx={{ mb: 3 }} />
      </Box>

      <Box sx={{ px: { xs: 0, sm: 1 } }}>
        <VideoItemSkeleton />
        <VideoItemSkeleton />
        <VideoItemSkeleton />
      </Box>

      <Paper
        sx={{
          p: 3,
          mt: 4,
          bgcolor: "rgba(0, 0, 0, 0.02)",
          borderRadius: 2,
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            flexWrap: "wrap",
          }}
        >
          <Skeleton variant="text" sx={{ width: "40%", height: 24 }} />
          <Skeleton variant="text" sx={{ width: "40%", height: 24 }} />
        </Box>
      </Paper>
    </Paper>
  );
};

const VideoListSkeleton: React.FC<VideoListSkeletonProps> = ({ count = 2 }) => {
  return (
    <Box sx={{ mt: 5 }}>
      <Skeleton
        variant="text"
        sx={{ width: "40%", height: 40, mb: 4, ml: 1 }}
      />

      {Array.from(new Array(count)).map((_, index) => (
        <CombinationSkeleton key={index} />
      ))}
    </Box>
  );
};

export default VideoListSkeleton;
