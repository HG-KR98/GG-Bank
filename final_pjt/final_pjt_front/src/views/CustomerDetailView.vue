<template>
  <div>
    <h1>고객과의 소통 상세 페이지</h1>
    <div v-if="article">
      <p>{{ article.id }}</p>
      <p>{{ article.title }}</p>
      <p>{{ article.content }}</p>
      <p>{{ article.created_at }}</p>
      <p>{{ article.updated_at }}</p>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute } from "vue-router";

const store = useCounterStore();
const route = useRoute();
const article = ref(null);

onMounted(() => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/customer_articles/${route.params.id}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      article.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
});
</script>

<style scoped></style>
