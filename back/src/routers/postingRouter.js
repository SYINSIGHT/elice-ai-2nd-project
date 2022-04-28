import express from "express";
import Postings from "../../db/models/postings";
import mysqlManager from "../../db";
import Sequelize from "sequelize";

const postingRouter = express.Router();

// Posting Create
postingRouter.post("/postings/posting", async function (req, res, next) {
  try {
    const posting = {
      usersId: req.body.usersId,
      title: req.body.title,
      article: req.body.article,
      file_url: req.body.file_url,
    };
    
    const result = await Postings.create(posting)
    res.send(result);
  } catch (error) {
    console.log(error)
    console.log("게시글 등록 실패");
  }
});

//create한 다음에 게시판 목록 페이지로 가게 하고싶음
postingRouter.get("/postings", async function (req, res, next) {
  Postings.findAll().then((result) => {
    res.render("show", {
      postings: result,
    });
  });
});

// Posting 1개 Get
postingRouter.get("/postings/:id", async function (req, res, next) {
  try {
    const id = req.params.id;
    Postings.findOne({
      where: { id: id },
    }).then((result) => {
      posting: result;
      console.log(`게시물 postingId - ${id}`);
    });
  } catch (error) {
    console.log(error);
  }
});

// Posting Update
postingRouter.put("/postings/:id", async function (req, res, next) {
  try {
    const id = req.params.id;

    Postings.update(
      {
        usersId: req.body.usersId,
        title: req.body.title,
        article: req.body.article,
        file_url: req.body.file_url,
      },
      {
        where: { id: id },
      },
    ).then((result) => {
      console.log("게시글 수정 완료");
      res.redirect("/postings");
    });
  } catch (error) {
    console.log(`${error} - 게시글 수정 실패`);
  }
});

// Posting Delete
postingRouter.delete("/postings/:id", function (req, res, next) {
  const id = req.params.id;

  Postings.destroy({
    where: { id: id },
  })
    .then((result) => {
      res.redirect("/postings");
    })
    .catch((error) => {
      console.log("데이터 삭제 실패");
    });
});

export default postingRouter;
