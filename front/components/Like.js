import { useState } from "react";

import IconButton from "@mui/material/IconButton";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import FavoriteIcon from "@mui/icons-material/Favorite";

import * as Api from "../lib/api";

export default function Like({ postingsId, Likes }) {
  const loginUserId = "1911be41-3616-4cbb-8a82-cb962a9c"; // 임시

  // 로그인한 유저가 해당 post에 좋아요를 한 기록이 있는지
  let defaultLiked = false;
  Likes.forEach((likesObj) => {
    if (likesObj) {
      defaultLiked = Object.values(likesObj).includes(loginUserId);
    }
  });

  const [liked, setLiked] = useState(defaultLiked);

  const handleLikeClick = async () => {
    setLiked((liked) => !liked);
    // 원래 false면 post
    if (!liked) {
      try {
        await Api.post(`/postings/${postingsId}/like`);
      } catch (err) {
        console.error("좋아요에 실패했습니다.", err);
      }
      return;
    }

    // 원래 true면 delete
    try {
      await Api.delete(`/postings/${postingsId}/like`);
    } catch (err) {
      console.error("좋아요 취소에 실패했습니다.", err);
    }
  };

  // 조건 - 좋아요 유저 목록에 있는 id 중에 현재 로그인된 유저 id가 있는가
  return (
    <IconButton aria-label="like" onClick={handleLikeClick}>
      {liked ? <FavoriteIcon /> : <FavoriteBorderIcon />}
    </IconButton>
  );
}