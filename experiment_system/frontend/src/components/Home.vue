<template>
  <el-row justify="center" class="row">
    <el-col :span="12" class="inrow">
      <div>Student ID</div>
      <el-input v-model="store.student_id" placeholder="Student ID" />
      <div>Passcode</div>
      <el-input v-model="store.pass_code" placeholder="Passcode" />
      <el-button type="primary" @click="auth" :disabled="!screen"
        >Submit</el-button
      >
    </el-col>
  </el-row>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useStore } from "@/store";
import { useRouter, useRoute } from "vue-router";
import { useWindowSize } from "@vueuse/core";
import { ElMessage } from "element-plus";

import { useStorage } from "@vueuse/core";

const store = useStore();
const router = useRouter();

const screen = ref(true);
const state = useStorage("state", { uid: "", pass_code: "" });

onMounted(() => {
  const { width, height } = useWindowSize();
  // if (height.value < 1080) {
  //   screen.value = false;
  //   ElMessage({
  //     message: "Please use the screen's height more than 1080",
  //     duration: 0,
  //     type: "error",
  //   });
  // } else {
  store.width = width.value;
  store.height = height.value;
  if (state.value.uid && state.value.pass_code) {
    store.student_id = state.value.uid;
    store.pass_code = state.value.pass_code;
  }
  // }
});

const auth = async () => {
  // store.student_id = "";
  // store.pass_code = "";
  let auth_result = await store.auth();
  if (auth_result) {
    state.value.uid = store.student_id;
    state.value.pass_code = store.pass_code;
    console.log("auth_result", auth_result);
    router.push("/topics");
  }
};

// const check_auth = () => {
//   let auth_info = useStorage("auth");
//   console.log(auth_info.value);
//   return auth_info.value;
// };
</script>

<style scoped>
.row {
  height: 90vh;
}
.inrow {
  top: 50%;
}
</style>
