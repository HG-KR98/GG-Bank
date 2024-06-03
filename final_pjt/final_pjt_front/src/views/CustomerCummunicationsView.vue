<template>
  <div>
    <div class="title">
      <h2>고객과의 소통</h2>
    </div>
    <!-- <img src="@/assets/free_board.png" alt="이미지가 없습니다..." /> -->

    <!-- 검색창 -->
    <div class="search-box">
      <div class="input-group mb-3 mx-3">
        <button
          class="btn btn-secondary dropdown-toggle"
          type="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          선택
        </button>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" href="#">Action</a></li>
          <li><a class="dropdown-item" href="#">Another action</a></li>
          <li><a class="dropdown-item" href="#">Something else here</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="#">Separated link</a></li>
        </ul>
        <input
          type="text"
          class="form-control"
          placeholder="검색어를 입력해주세요."
          aria-label="Recipient's username with two button addons"
        />
        <button class="btn btn-primary" type="button">검색</button>
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
    <!-- 검색창 -->

    <!-- 글목록 -->
    <div id="board-list">
      <div class="container">
        <table class="table" id="user-table">
          <thead>
            <tr>
              <th width="5%" class="text-center">번호</th>
              <th width="35%" class="text-center">제목</th>
              <th width="15%" class="text-center">이름</th>
              <th width="15%" class="text-center">아이디</th>
              <th width="17%" class="text-center">작성일</th>
              <th width="13%" class="text-center">조회수</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(article, index) in store.customerArticles.slice(0, 3)"
              :key="article.id"
              class="article-list"
            >
              <th width="5%">{{ index + 1 }}</th>
              <th width="35%">
                <RouterLink
                  :to="{
                    name: 'CustomerDetailView',
                    params: { id: article.id },
                  }"
                >
                  {{ article.title }}
                </RouterLink>
              </th>
              <th width="15%">{{ article.created_at }}</th>
              <th width="15%"></th>
              <th width="17%">{{ article.user }}</th>
              <th width="13%"></th>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- 글목록 -->

    <!-- 글 페이지 이동 -->
    <nav aria-label="..." class="page-change">
      <ul class="pagination">
        <li class="page-item disabled">
          <a class="page-link">Previous</a>
        </li>
        <li class="page-item"><a class="page-link" href="#">1</a></li>
        <li class="page-item active" aria-current="page">
          <a class="page-link" href="#">2</a>
        </li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item">
          <a class="page-link" href="#">Next</a>
        </li>
      </ul>
    </nav>
    <!-- 글 페이지 이동 -->
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
</script>

<style scoped>
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
  height: 300px;
  background-color: white;
  margin: 20px 0;
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
}

.create-btn {
  text-decoration-line: none;
  color: white;
  font-weight: bold;
  font-size: 0.8rem; /* 글자 크기 */
  height: 30px; /* 높이 조정 */
  width: 30px; /* 너비 조정 */
}
</style>
