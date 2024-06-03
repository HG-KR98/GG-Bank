<template>
  <div>
    <form @submit.prevent="createArticle" class="create-form">
      <div class="card mt-5">
        <h1 class="card-header">게시글 작성</h1>
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
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useCounterStore();
// 게시글 인자 변수
const title = ref(null);
const content = ref(null);
const views = ref(0);
const image = ref(null);
const likes = ref(0);
const hates = ref(0);
const category = ref(null);
const createArticle = function () {
  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/articles/`,
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
      console.log(response);
      if (category.value === "free") {
        router.push({ name: "FreeArticlesView" });
      } else if (category.value === "investment") {
        router.push({ name: "InvestmentArticlesView" });
      } else {
        router.push({ name: "CustomerArticlesView" });
      }
    })
    .catch((error) => {
      console.log(error);
    });
};
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
