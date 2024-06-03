<template>
  <div class="parent">
    <div class="container">
      <div class="card smooth-box-style free">
        <div class="header card-header">
          <h3>자유게시판</h3>
          <RouterLink class="link-line" :to="{ name: 'FreeArticlesView' }"
            >더보기</RouterLink
          >
        </div>
        <div class="card-body">
          <table class="table">
            <thead>
              <tr>
                <th scope="col" width="10%">번호</th>
                <th scope="col" width="35%">제목</th>
                <th scope="col" width="15%">아이디</th>
                <th scope="col" width="17%">작성일</th>
                <th scope="col" width="13%">조회수</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(article, index) in cstore.articles.slice(0, 5)"
                :key="article.id"
              >
                <th scope="row">{{ index + 1 }}</th>
                <td>
                  <RouterLink
                    :to="{ name: 'FreeDetailView', params: { id: article.id } }"
                  >
                    {{ article.title }}
                  </RouterLink>
                </td>
                <td>{{ article.user.username }}</td>
                <td>{{ formatDate(article.created_at) }}</td>
                <td>{{ article.views }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card smooth-box-style money-tech">
        <div class="header card-header">
          <h3>재테크 정보공유</h3>
          <RouterLink class="link-line" :to="{ name: 'InvestmentArticlesView' }"
            >더보기</RouterLink
          >
        </div>
        <div class="card-body">
          <table class="table">
            <thead>
              <tr>
                <th scope="col" width="10%">번호</th>
                <th scope="col" width="35%">제목</th>
                <th scope="col" width="15%">아이디</th>
                <th scope="col" width="17%">작성일</th>
                <th scope="col" width="13%">조회수</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(article, index) in cstore.investmentArticles.slice(
                  0,
                  5
                )"
                :key="article.id"
              >
                <th scope="row">{{ index + 1 }}</th>
                <td>
                  <RouterLink
                    :to="{ name: 'FreeDetailView', params: { id: article.id } }"
                  >
                    {{ article.title }}
                  </RouterLink>
                </td>
                <td>{{ article.user.username }}</td>
                <td>{{ formatDate(article.created_at) }}</td>
                <td>{{ article.views }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card smooth-box-style customer">
        <div class="header card-header">
          <h3>고객과의 소통</h3>
          <RouterLink class="link-line" :to="{ name: 'CustomerArticlesView' }"
            >더보기</RouterLink
          >
        </div>
        <div class="card-body">
          <table class="table">
            <thead>
              <tr>
                <th scope="col" width="10%">번호</th>
                <th scope="col" width="35%">제목</th>
                <th scope="col" width="15%">아이디</th>
                <th scope="col" width="17%">작성일</th>
                <th scope="col" width="13%">조회수</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(article, index) in cstore.customerArticles.slice(0, 5)"
                :key="article.id"
              >
                <th scope="row">{{ index + 1 }}</th>
                <td>
                  <RouterLink
                    :to="{ name: 'FreeDetailView', params: { id: article.id } }"
                  >
                    {{ article.title }}
                  </RouterLink>
                </td>
                <td>{{ article.user.username }}</td>
                <td>{{ formatDate(article.created_at) }}</td>
                <td>{{ article.views }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useFinancialStore } from "@/stores/financial";
import { RouterLink } from "vue-router";

const cstore = useCounterStore();
const fstore = useFinancialStore();

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString(); // 원하는 형식으로 날짜를 포맷할 수 있습니다.
};

onMounted(() => {
  cstore.getArticles();
});
</script>

<style scoped>
.parent {
  display: flex;
  justify-content: center; /* 수평 중앙 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
  min-height: 70vh; /* 부모 컨테이너의 최소 높이를 설정 */
  margin-top: 20px;
}

.container {
  display: grid; /* 그리드 레이아웃을 사용하여 요소들을 배치합니다. */
  grid-template-columns: 2fr 1fr; /* 첫 번째 열은 두 번째 열의 두 배 너비를 가지도록 설정합니다. */
  grid-template-rows: 1fr 1fr 1fr; /* 각 행의 높이를 자동으로 설정합니다. */
  gap: 25px; /* 그리드 아이템 사이의 간격을 25px로 설정합니다. */
  min-height: 400px; /* 컨테이너의 최소 높이 설정 */
  padding-bottom: 50px; /* 푸터와의 간격을 벌리기 위한 패딩 */
}

.smooth-box-style {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.1);
}

.table {
  text-align: center;
}

.link-line {
  text-decoration-line: none;
  color: black;
}

.free {
  grid-column: 1 / 4; /* 이 아이템이 그리드의 첫 번째 열을 차지하도록 설정합니다. */
  grid-row: 1 / 2; /* 이 아이템이 그리드의 첫 번째 행을 차지하도록 설정합니다. */
  padding: 20px; /* 아이템의 안쪽 여백을 20px로 설정합니다. */
}

.money-tech {
  grid-column: 1 / 4; /* 이 아이템이 그리드의 두 번째 열을 차지하도록 설정합니다. */
  grid-row: 2 / 3; /* 이 아이템이 그리드의 첫 번째 행부터 두 번째 행까지 차지하도록 설정합니다. */
  padding: 20px; /* 아이템의 안쪽 여백을 20px로 설정합니다. */
}

.customer {
  grid-column: 1 / 4; /* 이 아이템이 그리드의 첫 번째 열을 차지하도록 설정합니다. */
  grid-row: 3 / 4; /* 이 아이템이 그리드의 두 번째 행을 차지하도록 설정합니다. */
  padding: 20px; /* 아이템의 안쪽 여백을 20px로 설정합니다. */
}
</style>
