<template>
  <div class="container">
    <div class="container-out">
      <div class="container-int">
        <img src="@/assets/free_board.png" alt="이미지가 없습니다..." />
        <Community />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import Community from "@/components/Community.vue";

const store = useCounterStore();

onMounted(() => {
  store.getArticles();
});
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  padding-top: 50px;
  padding-bottom: 50px;
}

.container-out {
  width: 100%;
  padding: 10px;
  min-width: 750px;
  border-radius: 15px;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.1);
  background-color: rgb(203, 230, 253);
}

img {
  border-radius: 15px; /* 테두리 둥글게 */
  width: 100%;
  height: 600px;
}

.card {
  margin: 20px 0;
}

.title {
  font-weight: bold;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.link-line {
  text-decoration-line: none;
  color: black;
  font-size: 15px;
}
</style>
