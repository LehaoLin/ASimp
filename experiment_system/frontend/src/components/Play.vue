<template>
  <div
    v-loading="loading"
    element-loading-text="Loading..."
    :element-loading-spinner="svg"
    element-loading-svg-view-box="-10, -10, 50, 50"
    element-loading-background="rgba(122, 122, 122, 1)"
  >
    <el-row>
      <el-col :span="12"></el-col>
      <el-col :span="12"
        ><el-slider v-model="rate2" :step="5" show-stops
      /></el-col>
    </el-row>
    <el-row class="model">
      <el-col :span="12">
        <model-viewer
          :key="fresh"
          @mousedown="view1_op"
          :src="url1 ? store.backend_url + url1.slice(1) : ''"
          ref="viewer1"
          data-js-focus-visible
          camera-controls
          disable-pan
          disable-tap
          disable-zoom
          interaction-prompt="none"
          touch-action="none"
          interpolation-decay="1"
          minimumRenderScale="1"
          max-camera-orbit="Infinity Infinity Infinity"
          min-camera-orbit="-Infinity -Infinity -Infinity"
          orientation="0deg 0deg 0deg"
        ></model-viewer>
      </el-col>
      <el-col :span="12">
        <model-viewer
          @mousedown="view2_op"
          :key="fresh"
          :src="url2 ? store.backend_url + url2.slice(1) : ''"
          ref="viewer2"
          data-js-focus-visible
          camera-controls
          disable-pan
          disable-tap
          disable-zoom
          interaction-prompt="none"
          touch-action="none"
          interpolation-decay="1"
          minimumRenderScale="1"
          max-camera-orbit="Infinity Infinity Infinity"
          min-camera-orbit="-Infinity -Infinity -Infinity"
          orientation="0deg 0deg 0deg"
        ></model-viewer>
      </el-col>
    </el-row>
    <el-row justify="space-around">
      <el-col :span="8">
        <center>
          <el-button @click="send_result('left')">Left is better</el-button>
        </center>
      </el-col>
      <el-col :span="8">
        <center>
          <el-button @click="send_result('no')">No difference</el-button>
        </center>
      </el-col>
      <el-col :span="8">
        <center>
          <el-button @click="send_result('right')">Right is better</el-button>
        </center>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ModelViewerElement } from "@google/model-viewer";
import { ref, onMounted } from "vue";
import axios from "axios";

import { useStore } from "@/store";
import { useRouter, useRoute } from "vue-router";

import { ElMessage } from "element-plus";

// max-camera-orbit="Infinity 90deg auto"
// min-camera-orbit="Infinity 90deg auto"

const store = useStore();
const router = useRouter();

const viewer1 = ref(null);
const viewer2 = ref(null);

const fresh = ref(0);

const rate1 = ref();
const rate2 = ref();

const url1 = ref();
const url2 = ref();

const swap = ref(false);

onMounted(async () => {
  await get_model();
});

const swap_url = () => {
  if (Math.random() < 0.5) {
    // swap
    swap.value = true;
    let temp;
    temp = url2.value;
    url2.value = url1.value;
    url1.value = temp;
  } else {
    swap.value = false;
  }
};

const view1_op = () => {
  viewer1.value.addEventListener("camera-change", view1toview2, true);
};

const view2_op = () => {
  viewer2.value.addEventListener("camera-change", view2toview1, true);
};

const view1toview2 = () => {
  try {
    viewer2.value.removeEventListener("camera-change", view2toview1, true);
  } catch (err) {
    console.log(err);
  }
  viewer2.value.cameraOrbit = viewer1.value.getCameraOrbit().toString();
};

const view2toview1 = () => {
  try {
    viewer1.value.removeEventListener("camera-change", view1toview2, true);
  } catch (err) {
    console.log(err);
  }
  viewer1.value.cameraOrbit = viewer2.value.getCameraOrbit().toString();
};

const sleep = (ms) => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

const loading = ref(false);

const check_loaded = async () => {
  while (true) {
    if (viewer1.value.modelIsVisible && viewer2.value.modelIsVisible) {
      fresh.value += 1;

      await sleep(2000);
      loading.value = false;
      break;
    } else {
      await sleep(500);
    }
  }
};

const start = ref(true);

const get_model = async () => {
  let msg;
  if (start.value) {
    msg = "start";
    rate1.value = store.rate1;
    rate2.value = 10;
    start.value = false;
  } else {
    msg = "continue";
  }
  let data = {
    topic: store.topic,
    msg,
    rate1: rate1.value,
    rate2: rate2.value,
  };
  let res = await axios({
    method: "post",
    url: store.backend_url + "/get_rate_url",
    data: data,
    withCredentials: true,
    mode: "no-cors",
  });
  rate1.value = res.data.rate1;
  rate2.value = res.data.rate2;
  url1.value = res.data.url1;
  url2.value = res.data.url2;
  console.log(url1.value);
  console.log(url2.value);
  swap_url();
  await check_loaded();
};

const send_result = async (direction) => {
  let better;
  if (swap.value) {
    if (direction == "left") {
      better = false;
    } else if (direction == "no") {
      better = false;
    } else if (direction == "right") {
      better = true;
    }
  } else {
    if (direction == "left") {
      better = true;
    } else if (direction == "no") {
      better = false;
    } else if (direction == "right") {
      better = false;
    }
  }
  let data = {
    topic: store.topic,
    rate1: rate1.value,
    rate2: rate2.value,
    better: better,
  };
  if (better) {
    ElMessage.success(`Correct! ${rate1.value}% vs ${rate2.value}%`);
  } else {
    ElMessage.error(`Wrong! ${rate1.value}% vs ${rate2.value}%`);
  }
  let res = await axios({
    method: "post",
    url: store.backend_url + "/add_data",
    data: data,
    withCredentials: true,
    mode: "no-cors",
  });
  let res_ = await axios({
    method: "post",
    url: store.backend_url + "/next_round",
    data: {
      topic: store.topic,
      rate1: rate1.value,
      rate2: rate2.value,
      width: store.width,
      height: store.height,
    },
    withCredentials: true,
    mode: "no-cors",
  });
  if (res_.data.msg == "change topic") {
    router.push("/topics");
  } else {
    rate1.value = res_.data.rate1;
    rate2.value = res_.data.rate2;
    loading.value = true;
    await get_model();
    // loading.value = true;
    // await sleep(2000);
    // fresh.value += 1;
    // loading.value = false;
  }
};

const urls = ref([]);
const get_urls = async () => {
  let res = await axios({
    method: "post",
    url: store.backend_url + "/add_data",
    data: { topic: store.topic },
    withCredentials: true,
    mode: "no-cors",
  });
  urls.value = res.data.urls;
};
</script>

<style scoped>
.model {
  height: 95vh;
}
model-viewer {
  width: 100%;
  height: 100%;
  background-color: black;
}
</style>
