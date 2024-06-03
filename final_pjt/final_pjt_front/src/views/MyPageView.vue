<template>
  <div class="container">
    <div class="container-out-out m-2">
      <div class="sidebar-out m-2">
        <div class="sidebar-in">
          <ul>
            <li
              @click="showPage('info')"
              :class="{ active: currentPage === 'info' }"
              class="content-box"
            >
              기본 정보
            </li>
            <li
              @click="showPage('portfolio')"
              :class="{ active: currentPage === 'portfolio' }"
              class="content-box"
            >
              포트폴리오
            </li>
          </ul>
        </div>
      </div>

      <div class="content-in">
        <div v-if="currentPage === 'info'">
          <!-- 기본 정보 수정 페이지 내용 -->
          <div class="d-flex justify-content-between">
            <h2 class="font-weight-bold">기본 정보</h2>
            <div>
              <RouterLink class="link-line" :to="{ name: 'UpdateMyInfoView' }">
                <button class="btn btn-update me-3">수정하기</button>
              </RouterLink>
              <button class="btn btn-back" @click="goBack">뒤로가기</button>
            </div>
          </div>
          <div class="profile-section">
            <p class="border-bottom"></p>
            <div class="profile-info d-flex">
              <div class="img-section" style="width: 50%">
                <div class="profile-picture-editor">
                  <img
                    src="@/assets/GG-Logo.gif"
                    alt="Profile Picture"
                    class="profile-picture"
                  />
                </div>
              </div>
              <div class="content-section" style="width: 50%">
                <div class="info-item">
                  <label>아이디</label>
                  <span>{{ cstore.userInfo.username }}</span>
                </div>
                <div class="info-item">
                  <label>이메일</label>
                  <span>{{ cstore.userInfo.email }}</span>
                </div>
                <div class="info-item">
                  <label>이름</label>
                  <span>{{ cstore.userInfo.name }}</span>
                </div>
                <div class="info-item">
                  <label>생년월일</label>
                  <span>{{ cstore.userInfo.birth_date }}</span>
                </div>
                <div class="info-item">
                  <label>성별</label>
                  <span>{{ cstore.userInfo.gender }}</span>
                </div>
                <div class="info-item">
                  <label>자산</label>
                  <span>{{ cstore.userInfo.assets }} 원</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="currentPage === 'portfolio'">
          <!-- 포트폴리오 페이지 내용 -->
          <h2>{{ cstore.userInfo.name }}님의 포트폴리오</h2>
          <h4>현재 나의 자산 : {{ cstore.userInfo.assets }}원</h4>

          <!-- 포트폴리오 수정 내용 -->
          <div class="portfolio-list">
            <div
              v-for="portfolio in myPortFoilos"
              :key="portfolio.id"
              class="portfolio-item"
            >
              <div class="portfolio-header">
                <span class="portfolio-id">{{ portfolio.id }}</span
                >.
                <span class="portfolio-kind"
                  >({{ portfolio.product_kind }})</span
                >
                <span class="portfolio-company">{{ portfolio.kor_co_nm }}</span>
                -
                <span class="portfolio-name">{{ portfolio.fin_prdt_nm }}</span>
              </div>
              <div class="portfolio-assets">
                <span>1년 후 나의 자산 : </span>
                <span class="calculated-assets">
                  {{
                    cstore.userInfo.assets +
                    cstore.userInfo.assets * (portfolio.tweleve_month * 0.01)
                  }}
                  원
                </span>
                <!-- 포트폴리오 삭제 버튼 -->
                <button
                  class="btn btn-delete"
                  @click="deletePortFolio(portfolio.id)"
                >
                  삭제
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useFinancialStore } from "@/stores/financial";
import axios from "axios";
import { useRouter } from "vue-router";

// 라우터
const router = useRouter();

// portfolio 관련
const cstore = useCounterStore();
const fstore = useFinancialStore();
const currentPage = ref("info");
const myPortFoilos = ref([]);

const showPage = (page) => {
  currentPage.value = page;
};

const goBack = () => {
  window.history.back();
};

const getPortFolio = function () {
  axios({
    method: "get",
    url: `${fstore.API_URL}/financial_products/port_folio/`,
    headers: {
      Authorization: `Token ${cstore.token}`,
    },
  })
    .then((response) => {
      myPortFoilos.value = response.data.filter((item) => {
        return (
          fstore.depositBaseList.some(
            (baseitem) => baseitem.fin_prdt_cd === item.fin_prdt_cd
          ) ||
          fstore.savingBaseList.some(
            (baseitem) => baseitem.fin_prdt_cd === item.fin_prdt_cd
          )
        );
      });
      console.log(myPortFoilos);
    })
    .catch((error) => {
      console.log(error);
    });
};

const deletePortFolio = function (portfolioId) {
  axios({
    method: "delete",
    url: `${fstore.API_URL}/financial_products/port_folio/${portfolioId}/`,
    headers: {
      Authorization: `Token ${cstore.token}`,
    },
  })
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      console.log(error);
    });
  router.go(0);
};

onMounted(() => {
  getPortFolio();
});
</script>

<style scoped>
.container {
  padding-top: 50px;
  padding-bottom: 50px;
}

.container-out-out {
  display: flex;
  border-radius: 15px;
  background-color: rgb(203, 230, 253);
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
  align-items: center;
  min-width: 750px;
  border-radius: 15px;
  background-color: rgb(203, 230, 253);
}

.sidebar-in {
  margin-top: 50px;
  margin-bottom: 50px;
  border-radius: 15px;
  width: 200px;
  background-color: #f8f8f8;
  padding: 10px;
}

.sidebar-in ul {
  list-style: none;
  padding: 0;
}

.sidebar-in li {
  padding: 10px;
  cursor: pointer;
  text-align: center;
  border-radius: 15px;
  margin-bottom: 10px;
  background-color: #87cef2;
}

.sidebar-in li:hover,
.sidebar-in li.active {
  background-color: #6497fc;
}

.content-box {
  background-color: #85caff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 15px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 10px;
}

.content-box:hover {
  color: white;
  background-color: #64b5f6;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}

.content-in {
  flex: 1;
  height: 100%;
  padding: 20px;
  margin: 15px;
  border-radius: 15px;
  background-color: #ffffff;
}

.content-out {
  flex: 1;
  height: 100%;
  margin: 50px;
  border-radius: 15px;
  background-color: rgb(245, 245, 245);
}

.info-item {
  margin-bottom: 10px;
}

.info-item label {
  display: inline-block;
  width: 150px;
  font-weight: bold;
  background-color: white;
  border-radius: 15px;
  margin: 5px;
  font-size: 15px;
}

.info-item span {
  margin-right: 10px;
}

.edit-button,
.btn-edit {
  background-color: #93c47d;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 15px;
  margin-top: 10px;
}

.edit-button:hover,
.btn-edit:hover {
  background-color: #6aa84f;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}

.profile-picture-editor {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-picture {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.btn-update {
  background-color: #87cef2;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 15px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 10px;
}

.btn-update:hover {
  color: white;
  background-color: #64b5f6;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}

.btn-back {
  background-color: #c6e893;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 15px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 10px;
}

.btn-back:hover {
  color: white;
  background-color: #90f96d;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}

/* 추가된 포트폴리오 섹션 스타일 */
.portfolio-list {
  margin-top: 20px;
}

.portfolio-item {
  background-color: #f0f8ff;
  padding: 15px;
  border-radius: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.portfolio-header {
  font-weight: bold;
  font-size: 16px;
}

.portfolio-assets {
  margin-top: 10px;
}

.calculated-assets {
  font-weight: bold;
  color: #007bff;
}

.btn-delete {
  background-color: #c6e893;
  border: none;
}

.btn-delete:hover {
  background-color: #90f96d;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}
</style>
