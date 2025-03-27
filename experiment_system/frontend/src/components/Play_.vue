<template>
  <div
    v-loading="loading"
    element-loading-text="Loading..."
    :element-loading-spinner="svg"
    element-loading-svg-view-box="-10, -10, 50, 50"
    element-loading-background="rgba(122, 122, 122, 1)"
  >
    <el-row style="height: 4vh">
      <el-col :span="6"></el-col>
      <el-col :span="6">
        <center>
          <el-button @click="send_result()">Submit Result</el-button>
        </center></el-col
      >
      <el-col :span="1">{{ rate2 }}% </el-col>
      <el-col :span="8"
        ><el-slider
          v-model="rate2"
          :step="5"
          show-stops
          :min="5"
          @input="change"
      /></el-col>
      <!-- <el-col :span="3"><el-button @click="next()">Next</el-button></el-col> -->
    </el-row>
    <el-row class="model">
      <el-col :span="12">
        <model-viewer
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
          shadow-softness="0"
        >
          <div style="color: white">
            <div>
              Roll:
              <button @click="change_position('roll')">Change</button>
            </div>
            <div>
              Pitch:
              <button @click="change_position('pitch')">Change</button>
            </div>
            <div>
              Yaw:
              <button @click="change_position('yaw')">Change</button>
            </div>

            <button @click="update">updateFraming</button>
          </div>
        </model-viewer>
      </el-col>
      <el-col :span="12">
        <model-viewer
          @mousedown="view2_op"
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
          shadow-softness="0"
        >
          <div style="color: white">
            <div>
              Roll:
              <button @click="change_position('roll')">Change</button>
            </div>
            <div>
              Pitch:
              <button @click="change_position('pitch')">Change</button>
            </div>
            <div>
              Yaw:
              <button @click="change_position('yaw')">Change</button>
            </div>

            <button @click="update">updateFraming</button>
          </div>
        </model-viewer>
      </el-col>
    </el-row>
    <!-- <el-row justify="space-around">
      <el-col :span="8"> </el-col>
      <el-col :span="8">
        <center>
          <el-button @click="send_result()">Submit Result</el-button>
        </center>
      </el-col>
      <el-col :span="8"> </el-col>
    </el-row> -->
  </div>
</template>

<script setup>
import { ModelViewerElement } from "@google/model-viewer";
import { ref, onMounted, onUnmounted } from "vue";
import axios from "axios";

import { useStore } from "@/store";
import { useRouter, useRoute } from "vue-router";

import { ElMessage } from "element-plus";

import { ElNotification } from "element-plus";

import { useWindowSize } from "@vueuse/core";

const store = useStore();
const router = useRouter();

const viewer1 = ref(null);
const viewer2 = ref(null);

const fresh = ref(0);

const rate1 = ref();
const rate2 = ref();

const url1 = ref();
const url2 = ref();

const notify = ref();
const notify2 = ref();

const modelViewerTransform = ref();
const roll = ref(0);
const pitch = ref(0);
const yaw = ref(0);

onMounted(async () => {
  const { width, height } = useWindowSize();
  store.width = width.value;
  store.height = height.value;

  // modelViewerTransform.value = document.querySelector("model-viewer#transform");
  // roll.value = document.querySelector("#roll");
  // pitch.value = document.querySelector("#pitch");
  // yaw.value = document.querySelector("#yaw");

  // roll.value.addEventListener("input", () => {
  //   modelViewerTransform.value.orientation = `${roll.value.value}deg ${pitch.value.value}deg ${yaw.value.value}deg`;
  //   modelViewerTransform.value.updateFraming();
  // });
  // pitch.value.addEventListener("input", () => {
  //   modelViewerTransform.value.orientation = `${roll.value.value}deg ${pitch.value.value}deg ${yaw.value.value}deg`;
  //   modelViewerTransform.value.updateFraming();
  // });
  // yaw.value.addEventListener("input", () => {
  //   modelViewerTransform.value.orientation = `${roll.value.value}deg ${pitch.value.value}deg ${yaw.value.value}deg`;
  //   modelViewerTransform.value.updateFraming();
  // });

  notify.value = await ElNotification({
    title: "Attention",
    // message:
    //   "左侧为100%的模型，右侧为精度可变模型。滑动滑块更新模型精度，直至你认为以最小的百分比相较左侧模型【已经不再有显著进步】为止。如果在模型平面或底座出现因为减面出现的【褶皱】，请不要吹毛求疵，以观察模型的【主要部分】为主。",
    message: `Left side is a 100% model, while the right side is a model with adjustable precision. Slide the slider to update the model's resolution until you believe that there is no longer significant improvement compared to the model on the left. If there are "wrinkles" appearing due to reduction in resolution on the model, please don't nitpick, focus on observing the "main parts" of the model`,
    duration: 0,
    position: "top-left",
  });
  // notify2.value = await ElNotification({
  //   title: "提示",
  //   message:
  //     "如果你觉得模型放置有问题，左上角Change按钮调整，然后点击UpdateFraming按钮将镜头居中。如果左右模型旋转出现不同步，则也可以点击UpdateFraming进行矫正。",
  //   duration: 0,
  //   position: "top-left",
  // });
  //   await get_model();
  rate1.value = 100;
  rate2.value = 5;
  await get_urls();
  url1.value = urls.value.at(-1);
  url2.value = urls.value[0];
});

onUnmounted(() => {
  notify.value.close();
  notify2.value.close();
});

const view1_op = () => {
  viewer1.value.addEventListener("camera-change", view1toview2, true);
};

const view2_op = () => {
  viewer2.value.addEventListener("camera-change", view2toview1, true);
};

const change_position = (input) => {
  if (input == "roll") {
    roll.value += 90;
  } else if (input == "pitch") {
    pitch.value += 90;
  } else if (input == "yaw") {
    yaw.value += 90;
  }
  viewer1.value.orientation = `${roll.value}deg ${pitch.value}deg ${yaw.value}deg`;
  viewer2.value.orientation = `${roll.value}deg ${pitch.value}deg ${yaw.value}deg`;
};

const update = () => {
  viewer1.value.updateFraming();
  viewer2.value.updateFraming();
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

const next = async () => {
  if (rate2.value < 100) {
    rate2.value += 5;
  }
  await change();
};

const change = async () => {
  let index2 = rate2.value / 5 - 1;
  url2.value = urls.value[index2];
  fresh.value += 1;
};

const send_result = async () => {
  let data = {
    topic: store.topic,
    rate1: rate1.value,
    rate2: rate2.value,
    width: store.width,
    height: store.height,
  };
  let res = await axios({
    method: "post",
    url: store.backend_url + "/new_data",
    data: data,
    withCredentials: true,
    mode: "no-cors",
  });
  router.push("/topics");
};

const urls = ref([]);
const get_urls = async () => {
  let res = await axios({
    method: "post",
    url: store.backend_url + "/get_all_urls",
    data: { topic: store.topic },
    withCredentials: true,
    mode: "no-cors",
  });
  if (!res.data.auth) {
    router.push("/");
  }
  urls.value = res.data.urls;
  console.log(urls.value);
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
