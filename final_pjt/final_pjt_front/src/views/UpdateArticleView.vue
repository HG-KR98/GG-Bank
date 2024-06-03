<template>
  <div v-if="article">
    <form @submit.prevent="updateArticle" class="create-form">
      <div class="card mt-5">
        <h1 class="card-header">게시글 수정</h1>
        <div class="card-body">
          <div class="mb-3">
            <label for="title" class="form-label">제목</label>
            <input
              type="text"
              class="form-control"
              id="title"
              v-model="title"
              required
            />
          </div>
          <div class="mb-3">
            <label for="category" class="form-label">카테고리</label>
            <select
              class="form-select"
              id="category"
              v-model="category"
              required
            >
              <option value="">카테고리를 선택하세요</option>
              <option value="free">자유 게시판</option>
              <option value="investment">재테크 공유게시판</option>
              <option value="communication">고객과의 소통</option>
            </select>
          </div>
          <div class="mb-3">
            <label for="content" class="form-label">내용</label>
            <textarea
              class="form-control"
              id="content"
              v-model="content"
              rows="5"
              required
            ></textarea>
          </div>
          <input type="submit" value="제출" class="btn btn-primary" />
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const store = useCounterStore();
// 기존 게시글 정보
const article = ref(null);

const title = ref(null);
const content = ref(null);
const views = ref(0);
const image = ref(null);
const category = ref(null);

// 업데이트 함수
const updateArticle = function () {
  axios({
    method: "put",
    url: `${store.API_URL}/api/v1/articles/detail/${article.value.id}/`,
    data: {
      title: title.value,
      content: content.value,
      views: views.value,
      image: image.value,
      category: category.value,
    },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      router.push({ name: "FreeDetailView", params: { id: article.value.id } });
    })
    .catch((error) => {
      console.log(error);
    });
};

onMounted(() => {
  if (route.params.category === "free") {
    console.log(
      store.articles.find((free) => free.id === parseInt(route.params.id))
    );
    article.value = store.articles.find(
      (free) => free.id === parseInt(route.params.id)
    );
  } else if (route.params.category === "investment") {
    article.value = store.investmentArticles.find(
      (investment) => investment.id === parseInt(route.params.id)
    );
  } else {
    article.value = store.customerArticles.find(
      (customer) => customer.id === parseInt(route.params.id)
    );
  }

  if (article) {
    title.value = article?.value.title;
    content.value = article?.value.content;
    views.value = article?.value.views;
    image.value = article?.value.image;
    category.value = article?.value.category;
  } else {
    console.error("Article not Found");
  }
});
</script>

<style scoped>
.text {
  height: 300px;
}

.card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.1);
}
</style>
