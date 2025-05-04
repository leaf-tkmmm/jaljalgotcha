import axios from "axios";
import { VideoCombination, ApiError } from "../types";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface GetCombinationsParams {
  duration: string;
  attempts?: number;
  useYoutube?: boolean;
}

export const getCombinations = async (
  params: GetCombinationsParams
): Promise<VideoCombination[]> => {
  try {
    const { duration, attempts = 3, useYoutube = false } = params;
    const response = await api.get<VideoCombination[]>("/combinations", {
      params: {
        duration,
        attempts,
        use_youtube: useYoutube,
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const apiError = error.response.data as ApiError;
      throw new Error(apiError.error || "Failed to fetch combinations");
    }
    throw new Error("An unexpected error occurred");
  }
};
