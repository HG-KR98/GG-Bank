<template>
  <div class="container">
    <div class="container-out">
      <div class="container-in">
        <div class="selection-form m-2">
          <form @submit.prevent="submitForm">
            <div class="form-group underline">
              <label>성별</label>
              <div>
                <label>
                  <input type="radio" v-model="formData.gender" value="female" />
                  여자
                </label>
                <label>
                  <input type="radio" v-model="formData.gender" value="male" />
                  남자
                </label>
              </div>
            </div>

            <div class="form-group underline">
              <label>나이</label>
              <div>
                <label v-for="option in ageOptions" :key="option">
                  <input type="radio" :value="option" v-model="formData.age" />
                  {{ option }}
                </label>
              </div>
            </div>

            <div class="form-group underline">
              <label>연봉</label>
              <div>
                <label v-for="option in salaryOptions" :key="option">
                  <input type="radio" :value="option" v-model="formData.salary" />
                  {{ option }}
                </label>
              </div>
            </div>

            <div class="form-group underline">
              <label>자산</label>
              <div>
                <label v-for="option in assetOptions" :key="option">
                  <input type="radio" :value="option" v-model="formData.asset" />
                  {{ option }}
                </label>
              </div>
            </div>

            <div class="form-group">
              <label>저축성향</label>
              <div>
                <label v-for="option in tendencyOptions" :key="option">
                  <input
                    type="radio"
                    :value="option"
                    v-model="formData.tendency"
                  />
                  {{ option }}
                </label>
              </div>
            </div>

            <div class="btn-box">
              <button type="submit" class="btn">검색</button>
            </div>
          </form>
        </div>

        <div class="results">
          <h2>결과</h2>
          <table class="results-table">
            <thead>
              <tr>
                <th>제출월</th>
                <th>금융회사명</th>
                <th>상품명</th>
                <th>상품유형</th>
                <th v-if="formData.tendency === '단기'">6개월</th>
                <th v-if="formData.tendency !== '장기'">12개월</th>
                <th v-if="formData.tendency !== '단기'">24개월</th>
                <th v-if="formData.tendency === '장기'">36개월</th>
              </tr>
            </thead>
            <tbody>
              <template v-if="results && results.length">
                <tr v-for="result in filteredResults" :key="result.id">
                  <td>{{ result.dcls_month }}</td>
                  <td>{{ result.kor_co_nm }}</td>
                  <td>{{ result.fin_prdt_nm }}</td>
                  <td>{{ result.product_type }}</td>
                  <td v-if="formData.tendency === '단기'">{{ result.six_month }}</td>
                  <td v-if="formData.tendency !== '장기'">{{ result.twelve_month }}</td>
                  <td v-if="formData.tendency !== '단기'">{{ result.twenty_four_month }}</td>
                  <td v-if="formData.tendency === '장기'">{{ result.thirty_six_month }}</td>
                </tr>
              </template>
              <template v-else>
                <tr>
                  <td colspan="8">조회 결과가 없습니다.</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const store = useCounterStore();

const formData = ref({
  gender: "",
  age: "",
  salary: "",
  asset: "",
  tendency: "",
});

const ageOptions = [
  "20세 미만",
  "20세 ~ 29세",
  "30세 ~ 39세",
  "40세 ~ 49세",
  "50세 ~ 59세",
  "60세 이상",
];

const salaryOptions = [
  "2000만원 미만",
  "2000만원 ~ 4000만원",
  "4000만원 ~ 6000만원",
  "6000만원 ~ 8000만원",
  "8000만원 ~ 1억원",
  "1억원 이상",
];

const assetOptions = [
  "2000만원 미만",
  "2000만원 ~ 6000만원",
  "6000만원 ~ 1억원",
  "1억원 ~ 2억원",
  "2억원 ~ 4억원",
  "4억원 이상",
];

const tendencyOptions = ["단기", "중기", "장기"];

const results = ref([]); // 빈 배열로 초기화

const submitForm = () => {
  const { gender, age, salary, asset, tendency } = formData.value;
  if (!gender || !age || !salary || !asset || !tendency) {
    alert("모든 옵션을 선택해주세요");
    return;
  }

  axios({
    method: "get",
    url: `${store.API_URL}/financial_products/algorithm/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    params: formData.value,
  })
    .then((response) => {
      console.log(response)
      const rawResults = response.data || []; // 데이터가 없으면 빈 배열 할당

      // 각 상품에 대한 옵션 데이터를 추가
      const optionsPromises = rawResults.map((result) => {
        return axios({
          method: "get",
          url: `${store.API_URL}/financial_products/deposit_options/${result.fin_prdt_cd}`,
          headers: {
            Authorization: `Token ${store.token}`,
          },
        }).then((optionResponse) => {
          const options = optionResponse.data;
          options.forEach(option => {
            if (option.save_trm === "6") result.six_month = option.intr_rate;
            if (option.save_trm === "12") result.twelve_month = option.intr_rate;
            if (option.save_trm === "24") result.twenty_four_month = option.intr_rate;
            if (option.save_trm === "36") result.thirty_six_month = option.intr_rate;
          });
          return result;
        });
      });

      Promise.all(optionsPromises).then((completedResults) => {
        results.value = completedResults;
      });
    })
    .catch((error) => {
      console.error("상품 조회 에러 발생:", error);
      results.value = []; // 오류 발생 시 빈 배열 할당
    });
};

const filteredResults = computed(() => {
  return results.value.filter(result => {
    if (formData.value.tendency === '단기') {
      return result.six_month || result.twelve_month;
    } else if (formData.value.tendency === '중기') {
      return result.twelve_month || result.twenty_four_month;
    } else if (formData.value.tendency === '장기') {
      return result.twenty_four_month || result.thirty_six_month;
    }
    return true;
  });
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

.container-in {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 750px;
  border-radius: 15px;
  background-color: rgb(203, 230, 253);
}

.selection-form,
.results {
  width: 100%;
  padding: 20px;
  border-radius: 15px;
  background-color: white;
}

.underline{
  border-bottom: 1px #DEE2E6 solid;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group div {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.btn-box {
  display: flex;
  justify-content: center;
}

.btn {
  width: 90%;
  background-color: #87CEF2;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 15px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
}

.btn:hover {
  color: white;
  background-color: #6497fc;
  transform: scale(1.05); /* 호버 시 약간 확대 */
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.results-table th,
.results-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.results-table th {
  background-color: #f2f2f2;
  text-align: center;
}

.results-table td {
  text-align: center;
}
</style>
