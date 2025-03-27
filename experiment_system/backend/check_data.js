import { db_connect, db_find } from "./db.js";

const check_uid = async () => {
  let db = await db_connect();
  let docs = await db_find(db, {});
  //   let temp = []
  let temp = docs.map((i) => i.uid);
  temp = Array.from(new Set(temp));
  console.log(temp);
  console.log(temp.length);
  let result = {};
  for (let uid of temp) {
    let record = await db_find(db, { uid: uid });
    result[uid] = record.length;
  }
  console.log(result);
  return temp;
};

await check_uid();
