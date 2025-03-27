import Datastore from "@seald-io/nedb";

import fs from "fs/promises";

const checkAndCreateFile = async (filePath) => {
  try {
    await fs.access(filePath, fs.constants.F_OK);
    console.log("File already exists.");
  } catch (error) {
    if (error.code === "ENOENT") {
      try {
        await fs.writeFile(filePath, "");
        console.log("File created successfully.");
      } catch (err) {
        console.error("Error creating the file:", err);
      }
    } else {
      console.error("Error checking file existence:", error);
    }
  }
};

export const db_connect =() => {
  // await checkAndCreateFile("./data/data.db");
  const db = new Datastore({ filename: "./data/data.db", autoload: true });
  return db;
};

export const db2_connect = () => {
  // await checkAndCreateFile("./data/finish.db");
  const db = new Datastore({ filename: "./data/finish.db", autoload: true });
  return db;
};

export const db_insert = async (db, data) => {
  try {
    const newDoc = await db.insertAsync(data);
  } catch (err) {
    console.log(err);
  }
};

export const db_find = async (db, data) => {
  const docs = await db.findAsync(data);
  return docs;
};

export const db_remove = async (db, data) => {
  try {
   await db.removeAsync(data, { multi: true })
    console.log(`Removed`)
  } catch (err){
    console.log(err)
  }
}

// const docs = await db.findAsync({ hello: "world" });

// console.log(docs);
