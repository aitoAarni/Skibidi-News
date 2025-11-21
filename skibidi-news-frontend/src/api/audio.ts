import axios from "axios";
import { endpoints } from "./config";

export type StudioResult = {
  transcript: string;
  video_id: string;
  video_url: string;
};

export const generateStudioAsset = async (
  humorText: string,
  backgroundVideo: string = "subway-surfers"
): Promise<StudioResult> => {
  const { data } = await axios.post(endpoints.studioGenerate, {
    humor_text: humorText,
    background_video: backgroundVideo,
  });

  const rawUrl = data.video_url;
  const videoUrl =
    typeof rawUrl === "string"
      ? rawUrl
      : rawUrl?._url ?? endpoints.studioVideo(data.video_id);

  return {
    transcript: data.transcript,
    video_id: data.video_id,
    video_url: videoUrl,
  };
};
