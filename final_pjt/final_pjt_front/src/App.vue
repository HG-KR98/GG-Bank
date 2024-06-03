<template>
  <div>
    <!-- 헤더 = 서브 바 + 내브 바 -->
    <div class="header">
      <div class="col-8 offset-sm-2">
        <!-- 서브 바 -->
        <nav class="sub-bar">
          <div class="sub-menu">
            <template v-if="store.isLogin">
              <RouterLink
                :to="{ name: 'MyPageView' }"
                class="bar button"
                style="font-weight: bold"
                >마이 페이지</RouterLink
              >
              <button class="button" @click="logout">로그아웃</button>
            </template>
            <template v-else>
              <RouterLink
                :to="{ name: 'LogInView' }"
                class="bar button"
                style="font-weight: bold"
                >로그인</RouterLink
              >
              <RouterLink
                :to="{ name: 'SignUpView' }"
                class="bar button"
                style="font-weight: bold"
                >회원가입</RouterLink
              >
            </template>
          </div>
        </nav>

        <!-- 내브 바 -->
        <nav class="navbar custom-hr">
          <a href="http://localhost:5173/">
            <img
              src="@/assets/GG-Logo.gif"
              alt="no-image"
              width="100px"
              height="100px"
            />
          </a>

          <RouterLink class="Bars" :to="{ name: 'DepositListView'}">투자 상품 비교</RouterLink>
          <RouterLink class="Bars" :to="{ name: 'ExchangeRateView' }"
            >환율 계산기</RouterLink
          >
          <RouterLink class="Bars" :to="{ name: 'FindBankView' }"
            >근처 은행 검색</RouterLink
          >
          <RouterLink class="Bars" :to="{ name: 'ArticleView' }"
            >커뮤니티</RouterLink
          >
          <RouterLink class="Bars" :to="{ name: 'AlgorithmView'}"
          >저축 상품 추천</RouterLink>
        </nav>
      </div>

      <!-- 라우터 뷰 -->
      <div class="middle">
        <div class="col-8 offset-sm-2 container">
          <RouterView />
        </div>
      </div>
      <!-- 라우터 뷰 -->

      <!-- 푸터 -->
      <footer class="">
        <div class="footer-content">
          <ul>
            <li><a href="#">이용약관</a></li>
            <li><a href="#">개인정보 처리방침</a></li>
            <li><a href="#">문의하기</a></li>
          </ul>
        </div>
        <div class="footer-bottom">
          <p>&copy; Copyright GG Bank, All Rights Reserved.</p>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

const store = useCounterStore();
const router = useRouter();

const logout = function () {
  store.token = null;
  router.push({ name: "LogInView" });
};
</script>

<style scoped>
/* .middle 스타일 */
.middle {
  background-color: rgb(227, 243, 250);
  border-top: 5px solid #6497fc; /* 선의 두께와 색상 설정 */
  margin-top: 20px; /* 위아래 여백 설정 */
}

/* 우측 상단에 위치 시키기 */
.sub-bar {
  position: absolute;
  top: 15px;
  right: 10px;
  padding: 4px;
  height: 20px;
}

.sub-menu {
  display: flex; /* RouterLink와 로그아웃 버튼 한 줄로 나열 */
  gap: 10px;
  align-items: center;
  margin-top: 15px;
}

/* nav 스타일 */
nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 105px;
  padding: 0 20px;
  text-align: center;
}

/* nav bar 스타일 */
.Bars {
  text-decoration-line: none; /* 밑줄 제거 */
  padding: 20px;
  margin: 0 10px;
  color: black;
  font-weight: bold;
  font-size: large;
}

/* sub-bar 스타일 */
.bar {
  padding: 5px;
  text-decoration-line: none;
  color: gray;
}

/* 버튼 */
.button {
  background-color: #87CEF2;
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
  transform: scale(1.1); /* 호버 시 약간 확대 */
}

/* 푸터 */
.footer-container {
  bottom: 0px;
}

footer {
  background-color: #333;
  color: #fff;
  padding-top: 20px;
  text-align: center;
}

.footer-content ul {
  list-style: none;
  padding: 0;
}

/* 한 줄로 표시 및 간격 조정 */
.footer-content ul li {
  display: inline;
  margin-right: 20px;
}

/* 하이퍼링크 파란색 제거 */
.footer-content ul li a {
  color: #fff;
  text-decoration: none;
}

.footer-bottom {
  background-color: #222;
  padding: 10px 0;
}

/* @import "bootstrap/dist/css/bootstrap.min.css"; */
.container {
  min-height: 800px;
}
</style>
