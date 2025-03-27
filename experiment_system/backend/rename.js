import fs from "fs/promises";

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

async function renameFile(oldFileName, newFileName) {
  try {
    await fs.rename(oldFileName, newFileName);
    // console.log("File renamed successfully");
  } catch (err) {
    console.error(err);
  }
}
async function renameDirectory(oldDirectoryName, newDirectoryName) {
  try {
    await fs.rename(oldDirectoryName, newDirectoryName);
    // console.log("Directory renamed successfully");
  } catch (err) {
    console.error(err);
  }
}

export const rename = async () => {
  let results = await all_topics();
  results = results.filter((i) => i != ".DS_Store");
  for (let topic of results) {
    let files = await listDirectoryContents(`./3dmodels/${topic}`);
    for (let i = 0; i < files.length; i++) {
      await renameFile(
        `./3dmodels/${topic}/${files[i]}`,
        `./3dmodels/${topic}/${files[i].replaceAll(" ", "_")}`
      );
    }
  }
  for (let i = 0; i < results.length; i++) {
    await renameDirectory(
      `./3dmodels/${results[i]}`,
      `./3dmodels/${results[i].replaceAll(" ", "_")}`
    );
  }
  console.log("Rename finish");
};
