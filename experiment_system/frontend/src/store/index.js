import { defineStore } from "pinia";
import axios from "axios";

export const useStore = defineStore("store", {
  state: () => {
    return {
      student_id: "",
      pass_code: "",
      all_topics: [],
      topic: "",
      rate1: 100,
      backend_url: "http://localhost:4444",

      height: 0,
      width: 0,
    };
  },
  getters: {},
  actions: {
    check_auth() {},
    async auth() {
      if (this.student_id && this.pass_code) {
        let res = await axios({
          method: "post",
          url: this.backend_url + "/auth",
          data: {
            uid: this.student_id,
            pass_code: this.pass_code,
          },
          withCredentials: true,
          mode: "no-cors",
        });
        console.log(res.data.auth);
        return res.data.auth;
      }
    },
    async get_all_topics() {
      let res = await axios({
        method: "post",
        url: this.backend_url + "/all_topics",
        data: {},
        withCredentials: true,
        mode: "no-cors",
      });
      console.log(res.data);
      this.all_topics = res.data.topics;
    },
    async check_finish() {
      let result = [];
      if (this.all_topics.length != 0) {
        for (let topic of this.all_topics) {
          let res = await axios({
            method: "post",
            url: this.backend_url + "/check_finish",
            data: {
              uid: this.student_id,
              topic: topic,
            },
            withCredentials: true,
            mode: "no-cors",
          });
          console.log(res.data);

          result.push({
            topic,
            result: res.data.result,
            // results100: res.data.results100,
            // results90: res.data.results90,
            // results80: res.data.results80,
          });

          //   res.data.msg
          //     ? result.push({ topic: topic, results100: })
          //     : result.push({ topic: topic, finish: false });
        }
        // result = this.all_topics.map(async (i) => {
        //   let res = await axios({
        //     method: "post",
        //     url: backend_url + "/check_finish",
        //     data: {
        //       uid: this.student_id,
        //       topic: i,
        //     },
        //     withCredentials: true,
        //     mode: "no-cors",
        //   });
        //   return res.data.msg
        //     ? { topic: i, finish: true }
        //     : { topic: i, finish: false };

        return result;
      }
    },
  },
});
