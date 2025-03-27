import express from "express";
import cors from "cors";
import dayjs from "dayjs";
import { get_model_path, all_topics, check_stop } from "./choice.js";
import { check_auth } from "./auth.js";
import {
  db_connect,
  db2_connect,
  db_insert,
  db_find,
  db_remove,
} from "./db.js";
import cookieParser from "cookie-parser";

import { rename } from "./rename.js";

const app = express();

const allowedOrigin = [
  "http://localhost:5173",
  "http://localhost:5174",
  "http://10.20.18.58:5173",
]; // Replace with your domain
const corsOptions = {
  origin: allowedOrigin,
  credentials: true,
};
app.use(cors(corsOptions));
const port = 4444;

app.use(express.json());
app.use("/3dmodels", express.static("3dmodels"));
app.use(cookieParser());

import session from "express-session";
import FileStore from "session-file-store";
const FileStoreInstance = FileStore(session);

app.use(
  session({
    store: new FileStoreInstance(),
    secret: "keyboard cat dog cat dog cat",
    resave: true,
    saveUninitialized: true,
    reapInterval: -1,
    cookie: { maxAge: 60 * 60 * 24 * 365 },
  })
);

const db = db_connect();
const db2 = db2_connect();

app.get("/", async (req, res) => {
  let now = dayjs().format();
  console.log(now);
  return res.json({ status: 1, time: now });
});

app.post("/auth", async (req, res) => {
  console.log("auth");
  let request = req.body;
  console.log(request);
  if (check_auth(request.uid, request.pass_code)) {
    req.session.uid = request.uid;
    req.session.auth = true;
    return res.json({ auth: true });
  } else {
    req.session.auth = false;
    return res.json({ auth: false });
  }
});

app.post("/all_topics", async (req, res) => {
  if (!req.session.auth) {
    return res.json({ auth: false });
  }
  let topics = await all_topics();
  return res.json({ auth: true, topics });
});

app.post("/next_round", async (req, res) => {
  if (!req.session.auth) {
    return res.json({ auth: false });
  }
  let uid = req.session.uid;
  let request = req.body;
  let topic = request.topic;
  let rate1 = request.rate1;
  let rate2 = request.rate2;
  let width = request.width;
  let height = request.height;
  let docs = await db_find(db, { uid, topic, rate1, rate2 });
  if (docs.length < 3) {
    // next round
    return res.json({ auth: true, topic, rate1, rate2 });
  } else {
    // next rate
    let check = await check_stop(
      db,
      db2,
      uid,
      topic,
      rate1,
      rate2,
      width,
      height
    );
    if (!check) {
      // stop, change topic
      return res.json({ auth: true, msg: "change topic" });
    } else {
      // not stop, change rate
      return res.json({ auth: true, uid, topic, rate1, rate2: rate2 + 10 });
    }
  }
});

app.post("/get_model_path", async (req, res) => {
  if (!req.session.auth) {
    return res.json({ auth: false });
  }
  let request = req.body;
  let topic = request.topic;
  let rate = request.rate;
  let model_path = get_model_path(topic, rate);
  return res.json({ auth: true, model_path });
});

app.post("/add_data", async (req, res) => {
  if (!req.session.auth) {
    return res.json({ auth: false });
  }
  let uid = req.session.uid;
  let time = dayjs().format();
  let request = req.body;
  let topic = request.topic;
  let rate1 = request.rate1; // better real
  let rate2 = request.rate2;
  let better = request.better; // true false
  console.log(better);
  //   let judge = better == rate1 ? true : false;
  //   let round = request.round;
  await db_insert(db, { topic, rate1, rate2, better, time, uid });
  return res.json({ auth: true });
});

app.post("/check_data", async (req, res) => {
  if (!req.session.auth) {
    return res.json({ auth: false });
  }
  let uid = req.session.uid;
  let topic = request.topic;
  let rate1 = request.rate1;
  let rate2 = request.rate2;
  let result = await db_find(db, { uid, topic, rate1, rate2 });
  if (result.length < 3) {
    return res.json({ auth: true, msg: true });
  } else {
    return res.json({ auth: true, msg: false });
  }
});

app.post("/get_rate_url", async (req, res) => {
  if (!req.session.auth) {
    return res.json({ auth: false });
  }
  let ctx = { auth: true };
  let uid = req.session.uid;
  let request = req.body;
  let topic = request.topic;
  let rate1 = request.rate1;
  let rate2 = request.rate2;

  if (request.msg == "start") {
    ctx.rate1 = rate1;
    ctx.rate2 = rate2;

    let pre_records = await db_find(db, { uid, topic, rate2 });
    if (pre_records.length > 0) {
      await db_remove(db, { uid, topic });
    }
    ctx.url1 = await get_model_path(topic, ctx.rate1);
    ctx.url2 = await get_model_path(topic, ctx.rate2);
    return res.json(ctx);
  } else if (request.msg == "continue") {
    console.log(rate1, rate2);
    ctx.rate1 = rate1;
    ctx.rate2 = rate2;
    ctx.url1 = await get_model_path(topic, rate1);
    ctx.url2 = await get_model_path(topic, rate2);
    return res.json(ctx);
  }
});

rename();

app.post("/check_finish", async (req, res) => {
  if (!req.session.auth) {
    return res.json({ auth: false });
  }
  let request = req.body;
  let uid = req.session.uid;
  let topic = request.topic;
  let result = await db_find(db, { uid, topic });
  result = result.length != 0 ? true : false;
  return res.json({ auth: true, result });
});

app.post("/new_data", async (req, res) => {
  if (!req.session.auth) {
    return res.json({ auth: false });
  }
  let uid = req.session.uid;
  let request = req.body;
  let topic = request.topic;
  let time = dayjs().format();
  let rate1 = request.rate1;
  let rate2 = request.rate2;
  let width = request.width;
  let height = request.height;
  await db_insert(db, { topic, rate1, rate2, width, height, uid, time });
  console.log({ topic, uid });
  return res.json({ auth: true });
});

app.post("/get_all_urls", async (req, res) => {
  if (!req.session.auth) {
    return res.json({ auth: false });
  }
  let request = req.body;
  let topic = request.topic;
  let urls = [];
  for (let i = 5; i <= 100; i += 5) {
    let url = await get_model_path(topic, i);
    urls.push(url);
  }
  return res.json({ auth: true, urls: urls });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
