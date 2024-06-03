<template>
  <div v-if="data" class="container-out">
    <div class="container-in">
      <div class="search-section">
        <h2 style="padding-bottom: 5px; border-bottom: 1px solid gray">
          검색하기
        </h2>

        <!-- 은행 선택 -->
        <div class="form-group">
          <label for="bank">은행을 선택하세요</label>
          <select id="bank" v-model="bank" class="form-control">
            <option value="">전체은행</option>
            <option value="우리은행">우리은행</option>
            <option value="한국스탠다드차타드은행">
              한국스탠다드차타드은행
            </option>
            <option value="대구은행">대구은행</option>
            <option value="부산은행">부산은행</option>
            <option value="광주은행">광주은행</option>
            <option value="제주은행">제주은행</option>
            <option value="전북은행">전북은행</option>
            <option value="경남은행">경남은행</option>
            <option value="중소기업은행">중소기업은행</option>
            <option value="한국산업은행">한국산업은행</option>
            <option value="국민은행">국민은행</option>
            <option value="신한은행">신한은행</option>
            <option value="농협은행주식회사">농협은행주식회사</option>
            <option value="하나은행">하나은행</option>
            <option value="주식회사 케이뱅크">주식회사 케이뱅크</option>
            <option value="수협은행">수협은행</option>
            <option value="주식회사 카카오뱅크">주식회사 카카오뱅크</option>
            <option value="토스뱅크 주식회사">토스뱅크 주식회사</option>
          </select>
        </div>

        <!-- 조회 버튼 -->
        <button
          type="submit"
          class="link-btn"
          @click="search"
          style="width: 100%"
        >
          조회
        </button>
      </div>

      <!-- 결과 영역 -->
      <div class="result-section">
        <div class="d-flex justify-content-between nav-buttons">
          <h2>정기예금</h2>
          <div>
            <button type="button" class="link-btn">
              <RouterLink :to="{ name: 'DepositListView' }" class="link"
                >정기예금</RouterLink
              >
            </button>
            <button type="button" class="link-btn">
              <RouterLink :to="{ name: 'SavingListView' }" class="link"
                >정기적금</RouterLink
              >
            </button>
          </div>
        </div>
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>공시 제출월</th>
                <th>금융회사명</th>
                <th>상품명</th>
                <th>
                  6개월
                  <button class="up-btn" @click="sortData('6', 'asc')">
                    ↑
                  </button>
                  <button class="down-btn" @click="sortData('6', 'desc')">
                    ↓
                  </button>
                </th>
                <th>
                  12개월
                  <button class="up-btn" @click="sortData('12', 'asc')">
                    ↑
                  </button>
                  <button class="down-btn" @click="sortData('12', 'desc')">
                    ↓
                  </button>
                </th>
                <th>
                  24개월
                  <button class="up-btn" @click="sortData('24', 'asc')">
                    ↑
                  </button>
                  <button class="down-btn" @click="sortData('24', 'desc')">
                    ↓
                  </button>
                </th>
                <th>
                  36개월
                  <button class="up-btn" @click="sortData('36', 'asc')">
                    ↑
                  </button>
                  <button class="down-btn" @click="sortData('36', 'desc')">
                    ↓
                  </button>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="deposit in data" :key="deposit.id">
                <td>{{ deposit.dcls_month }}</td>
                <td>{{ deposit.kor_co_nm }}</td>
                <td>
                  <RouterLink
                    :to="{
                      name: 'DepositDetailView',
                      params: { fin_prdt_cd: deposit.fin_prdt_cd },
                    }"
                    class="link-line"
                  >
                    {{ deposit.fin_prdt_nm }}</RouterLink
                  >
                </td>
                <td>{{ deposit["6"] }}</td>
                <td>{{ deposit["12"] }}</td>
                <td>{{ deposit["24"] }}</td>
                <td>{{ deposit["36"] }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useFinancialStore } from "@/stores/financial";
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

const store = useFinancialStore();
const bank = ref("");
const period = ref("");
const data = ref([]);

// 검색 메서드
const search = () => {
  data.value = store.depositBaseList.filter((deposit) => {
    return (
      (bank.value === "" || deposit.kor_co_nm === bank.value) &&
      (period.value === "" || deposit[period.value] !== undefined)
    );
  });
};

// 데이터 정렬 메서드
const sortData = (period, order) => {
  const sortOrder = order === "asc" ? 1 : -1;
  data.value.sort((a, b) => (a[period] - b[period]) * sortOrder);
};

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(() => {
  store.getDepositBaseList();
  data.value = store.depositBaseList;
});
</script>

<style scoped>
.nav-buttons {
  margin: 20px 0;
}

.link-btn {
  background-color: #87cef2;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 15px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  margin-right: 10px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.link-line {
  text-decoration-line: none;
}

.link-btn:hover {
  background-color: #6497fc;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}

.link {
  text-decoration: none;
  color: #ffffff;
  font-weight: bold;
}

.container-out {
  width: 100%;
  margin-top: 50px;
  margin-bottom: 50px;
  padding: 10px;
  min-width: 750px;
  border-radius: 15px;
  background-color: rgb(203, 230, 253);
}
.container-in {
  display: flex;
  justify-content: space-between;
  min-width: 750px;
  border-radius: 15px;
  background-color: rgb(203, 230, 253);
}
.search-section {
  width: 15%;
  min-height: 350px;
  background-color: aliceblue;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 15px;
}
.result-section {
  width: 84%;
  max-height: 600px;
  min-height: 350px;
  background-color: aliceblue;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 15px;
}
.table-responsive {
  max-height: 450px;
  overflow-y: auto; /* 세로 스크롤바 표시 */
}
.form-group {
  margin-bottom: 20px;
}
.btn {
  width: 100%;
  background-color: rgb(159, 230, 253);
}
/* 테이블 영역 */
.table {
  width: 100%;
}
.table th,
.table td {
  text-align: center;
  vertical-align: middle;
}

.up-btn {
  width: 30px;
  height: 30px;
  border-radius: 10px;
  border: none;
  color: white;
  background-color: rgb(255, 191, 191);
}

.up-btn:hover {
  color: white;
  background-color: rgb(252, 146, 146);
  transform: scale(1.2); /* 호버 시 약간 확대 */
}

.down-btn {
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 10px;
  border: none;
  background-color: #c6e893;
}

.down-btn:hover {
  color: white;
  background-color: #90f96d;
  transform: scale(1.2); /* 호버 시 약간 확대 */
}
</style>
