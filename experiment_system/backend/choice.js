import fs from "fs/promises";
import { db_find, db_insert } from "./db.js";

const listDirectoryContents = async (directoryPath) => {
  try {
    const files = await fs.readdir(directoryPath);
    // console.log(`Files and directories in ${directoryPath}:`);
    return files;
    // for (const file of files) {
    //   console.log(file);
    // }
  } catch (err) {
    console.error("Error reading directory:", err);
  }
};

export const all_topics = async () => {
  let files = await listDirectoryContents(`./3dmodels`);
  return files;
};

export const get_model_path = async (topic, rate) => {
  //   let dirs = await listDirectoryContents("./3dmodels");
  //   console.log(dirs);
  //   let target_dir = dirs.find((i) => i == topic);

  let files = await listDirectoryContents(`./3dmodels/${topic}`);

  let file_str = `${topic}_COLLAPSE_${rate}_`;

  let target_file = files.find((i) => {
    return i.includes(file_str);
  });

  return `./3dmodels/${topic}/${target_file}`;
};

const batch_judge = (results) => {
  let judge_arr = results.map((i) => (i.better ? 1 : 0));
  let judge_sum = judge_arr.reduce((a, b) => a + b, 0);
  if (judge_sum >= 2) {
    return true;
  } else {
    return false;
  }
};

export const check_stop = async (
  db,
  db2,
  uid,
  topic,
  rate1,
  rate2,
  width,
  height
) => {
  let results = await db_find(db, { uid, topic, rate1, rate2 });
  let judge_result = batch_judge(results);
  if (rate2 != 10) {
    // not first pk
    let results1 = await db_find(db, { uid, topic, rate1, rate2: rate2 - 10 });
    let judge_result1 = batch_judge(results1);
    if (rate1 == rate2) {
      await db_insert(db2, { uid, topic, rate1, width, height });
      return false;
    }
    if (!judge_result && !judge_result1) {
      await db_insert(db2, { uid, topic, rate1, width, height });
      return false;
    } else {
      return true;
    }
  } else {
    // first pk
    return true;
  }
};
