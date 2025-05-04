export interface Video {
  id: string;
  title: string;
  duration: number;
  duration_formatted: string;
  url?: string;
  thumbnail_url?: string;
}

export interface VideoCombination {
  videos: Video[];
  total_time: number;
  total_time_formatted: string;
  remaining_time: number;
  remaining_time_formatted: string;
}

export interface ApiError {
  error: string;
  hint?: string;
}
