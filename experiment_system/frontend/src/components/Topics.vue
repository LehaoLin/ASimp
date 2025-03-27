<template>
  <el-scroll height="90vh">
    <div v-for="(item, index) in topics" :key="index">
      <el-row justify="center">
        <el-col :span="4">
          <el-link
            v-if="item.topic != '.DS_Store'"
            :underline="false"
            :type="item.result ? 'danger' : 'success'"
            @click="select(item.topic, 100, item.result)"
            >{{ index + 1 }}-{{ item.topic }}</el-link
          >
        </el-col>
        <!-- <el-col :span="2">
          <center> -->
        <!-- <el-link
              v-if="item.topic != '.DS_Store'"
              :type="item.result ? 'danger' : 'success'"
              @click="select(item.topic, 100)"
              >[100]</el-link
            > -->
        <!-- &nbsp;
            <el-link
              v-if="item.topic != '.DS_Store'"
              :type="item.results90 ? 'danger' : 'success'"
              @click="select(item.topic, 90)"
              >[90]</el-link
            >
            &nbsp;
            <el-link
              v-if="item.topic != '.DS_Store'"
              :type="item.results80 ? 'danger' : 'success'"
              @click="select(item.topic, 80)"
              >[80]</el-link
            > -->
        <!-- </center>
        </el-col> -->
      </el-row>
    </div>
  </el-scroll>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useStore } from "@/store";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import { ElMessage } from "element-plus";

const store = useStore();
const router = useRouter();

const topics = ref([]);

onMounted(async () => {
  await store.get_all_topics();
  topics.value = await store.check_finish();
  console.log(topics.value);
  //   console.log(store.all_topics);
});

const select = async (topic, rate1, result) => {
  if (result) {
    ElMessage.error("该任务已经完成");
    return;
  }

  console.log(topic);
  store.topic = topic;
  store.rate1 = rate1;
  let res = await axios({
    method: "post",
    url: store.backend_url + "/check_finish",
    data: { topic: topic },
    withCredentials: true,
    mode: "no-cors",
  });
  if (!res.data.auth) {
    router.push("/");
  }
  if (res.data[`results${rate1}`]) {
    ElMessage.error("The topic is finished.");
  } else {
    router.push("/play");
  }
};
</script>

<style scoped></style>
