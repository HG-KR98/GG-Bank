<template>
  <div class="container">
    <div class="container-out">
      <div class="container-int">
        <img
          src="@/assets/freeArticle.png"
          alt="이미지가 없습니다..."
          class="title"
        />
        <!-- 검색창 -->
        <div class="search-box" style="border-radius: 15px">
          <div class="input-group mb-3 mx-3">
            <input
              type="text"
              class="form-control"
              placeholder="검색어를 입력해주세요."
              aria-label="Recipient's username with two button addons"
            />
            <button class="btn" type="button">검색</button>
          </div>

          <RouterLink
            class="icon-link icon-link-hover write-link"
            style="--bs-link-hover-color-rgb: 25, 135, 84"
            :to="{ name: 'CreateView' }"
          >
            글쓰기
            <svg class="bi" aria-hidden="true">
              <use xlink:href="#arrow-right"></use>
            </svg>
          </RouterLink>
        </div>

        <!-- 글목록 -->
        <div id="board-list">
          <div class="container">
            <table class="table" id="user-table">
              <thead>
                <tr>
                  <th width="5%" class="text-center">번호</th>
                  <th width="30%" class="text-center">제목</th>
                  <th width="15%" class="text-center">아이디</th>
                  <th width="17%" class="text-center">작성일</th>
                  <th width="13%" class="text-center">조회수</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(article, index) in paginatedArticles"
                  :key="article.id"
                  class="article-list"
                >
                  <th width="5%">{{ index + 1 }}</th>
                  <th width="30%">
                    <RouterLink
                      :to="{
                        name: 'FreeDetailView',
                        params: { id: article.id },
                      }"
                    >
                      {{ article.title }}
                    </RouterLink>
                  </th>
                  <th width="15%">{{ article.user.username }}</th>
                  <th width="17%">{{ formatDate(article.updated_at) }}</th>
                  <th width="13%">{{ article.views }}</th>
                  <!-- 여기에 좋아요 버튼 추가 -->
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 글 페이지 이동 -->
        <ul
          class="pagination d-flex justify-content-center align-items-center pb-3 mb-0"
        >
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="backPage">prev</button>
          </li>
          <li
            class="page-item"
            v-for="item in totalPages"
            :key="item"
            :class="{ active: currentPage === item }"
            :aria-current="currentPage === item ? 'page' : null"
          >
            <button class="page-link" @click="goToPage(item)">
              {{ item }}
            </button>
          </li>
          <li
            class="page-item"
            :class="{ disabled: currentPage === totalPages }"
          >
            <button class="page-link" @click="nextPage">next</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import { onMounted, ref, computed } from "vue";

const store = useCounterStore();
const perPage = ref(5);
const currentPage = ref(1);

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString(); // 또는 원하는 형식으로 날짜를 포맷할 수 있습니다.
};

// 현재 페이지에 해당하는 articles를 계산하는 computed
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * perPage.value;
  const end = start + perPage.value;
  console.log(store.articles);
  return store.articles.slice(start, end);
});

// 총 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(store.articles.length / perPage.value);
});

onMounted(() => {
  store.getArticles();
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value += 1;
  }
};

const backPage = () => {
  if (currentPage.value > 1) {
    currentPage.value -= 1;
  }
};

const goToPage = (numPage) => {
  currentPage.value = numPage;
};
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

.container-in {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 750px;
  border-radius: 15px;
  background-color: rgb(203, 230, 253);
}
.write-link {
  display: flex;
  align-items: center;
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
}

img {
  border-radius: 15px; /* 테두리 둥글게 */
  border: 1px solid #ccc; /* 테두리 색상 (선택 사항) */
  width: 100%;
  height: 600px;
}

.title {
  width: 100%;
  height: 500px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 15px;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.search-bar {
  margin: 20px 0;
}

.list-title {
  display: flex;
  justify-content: space-between;
}

.page-change {
  display: flex;
  justify-content: center;
}

.article-list {
  text-align: center;
}

.search-box {
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
}

.btn {
  background-color: #87cef2;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 15px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
}
.button:hover {
  background-color: #6497fc;
  color: black;
}

.form-control {
  /* 왼쪽 위 모서리에만 둥근 모서리 적용 */
  border-top-left-radius: 15px;

  /* 왼쪽 아래 모서리에만 둥근 모서리 적용 */
  border-bottom-left-radius: 15px;
}

.table {
  border-radius: 15px;
}
</style>
