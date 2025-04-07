import React, { forwardRef } from "react";
import { Typography, Paper, Box, Divider } from "@mui/material";
import VideoListItem from "./VideoListItem";
import { VideoCombination } from "../types";

interface VideoListProps {
  combinations: VideoCombination[];
}

const VideoList = forwardRef<HTMLDivElement, VideoListProps>(
  ({ combinations }, ref) => {
    if (combinations.length === 0) {
      return (
        <Paper
          sx={{
            p: 6,
            textAlign: "center",
            borderRadius: 2,
            boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
          }}
        >
          <Typography variant="subtitle1" sx={{ color: "text.secondary" }}>
            条件に合う組み合わせが見つかりませんでした。
          </Typography>
        </Paper>
      );
    }

    return (
      <Box sx={{ mt: 5 }} ref={ref}>
        <Typography
          variant="h5"
          component="h2"
          sx={{
            mb: { xs: 3, sm: 4 },
            fontWeight: "medium",
            color: "primary.main",
            pl: 1,
            fontSize: { xs: "1.25rem", sm: "1.5rem" },
          }}
        >
          動画の組み合わせ ({combinations.length})
        </Typography>

        {combinations.map((combo, index) => (
          <Paper
            key={index}
            sx={{
              p: { xs: 3, sm: 4 },
              mb: 4,
              borderRadius: 2,
              transition: "all 0.2s ease-in-out",
              boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
              "&:hover": {
                boxShadow: "0 8px 30px rgba(0,0,0,0.12)",
                transform: "translateY(-2px)",
              },
            }}
          >
            <Box sx={{ mb: 3 }}>
              <Typography
                variant="h6"
                sx={{
                  mb: 2,
                  fontWeight: "medium",
                  color: "text.primary",
                  fontSize: { xs: "1.125rem", sm: "1.25rem" },
                }}
              >
                組み合わせ {index + 1}
              </Typography>
              <Divider sx={{ mb: 3 }} />
            </Box>

            <Box sx={{ px: { xs: 0, sm: 1 } }}>
              {combo.videos.map((video) => (
                <VideoListItem key={video.id} video={video} />
              ))}
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
                  justifyContent: { xs: "flex-start", sm: "space-between" },
                  flexDirection: { xs: "column", sm: "row" },
                  flexWrap: "wrap",
                }}
              >
                <Typography
                  variant="body1"
                  sx={{
                    mr: 4,
                    fontWeight: "medium",
                    mb: { xs: 1, sm: 0 },
                    fontSize: { xs: "0.875rem", sm: "1rem" },
                  }}
                >
                  <strong>合計時間:</strong> {combo.total_time_formatted}
                </Typography>
                <Typography
                  variant="body1"
                  sx={{
                    fontWeight: "medium",
                    fontSize: { xs: "0.875rem", sm: "1rem" },
                  }}
                >
                  <strong>残り時間:</strong> {combo.remaining_time_formatted}
                </Typography>
              </Box>
            </Paper>
          </Paper>
        ))}
      </Box>
    );
  }
);

export default VideoList;
