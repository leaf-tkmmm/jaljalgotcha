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
}

export const getCombinations = async (
  params: GetCombinationsParams
): Promise<VideoCombination[]> => {
  try {
    console.log("getCombinationsのtryの中")
    const { duration, attempts = 3 } = params;
    const response = await api.get<VideoCombination[]>(`${import.meta.env.VITE_API_URL}/api/combinations`, {
      params: {
        duration,
        attempts
      },
    });
    console.log(response)
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const apiError = error.response.data as ApiError;
      throw new Error(apiError.error || "Failed to fetch combinations");
    }
    throw new Error("An unexpected error occurred");
  }
};
