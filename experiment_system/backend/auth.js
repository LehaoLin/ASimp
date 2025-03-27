export const check_auth = (id = "", passcode = "") => {
  let id_str = id.toString();
  passcode = passcode.toString();
  console.log(id_str, passcode);
  return true;
};
