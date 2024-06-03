<template>
  <div class="container">
    <div class="container-out">
      <div class="container-in">
        <!-- 이미지 -->
        <img
          src="@/assets/GG_Bank_Currency_Exchange_System.png"
          class="w-100"
          alt="ExchangePage"
        />

        <!-- 환율 계산기 폼 -->
        <div class="form">
          <div class="d-flex align-items-center" >
            <select class="form-select me-2" style="border-radius: 15px;">
              <option value="KRW">대한민국 원 (KRW)</option>
            </select>
            <input
              type="number"
              class="form-control"
              style="border-radius: 15px;"
              placeholder="금액 입력"
              v-model="won"
              @input="k_to_f"
            />
            <span class="ms-2">{{ formatted_won }} 원 (KRW) </span>
          </div>

          <!-- 두 번째 select와 입력 폼 -->
          <div class="d-flex align-items-center">
            <select class="form-select me-2" v-model="country" style="border-radius: 15px;">
              <option selected disabled>통화를 선택하세요</option>
              <option value="디르함 (AED)">아랍에미리트 디르함 (AED)</option>
              <option value="디나르 (AUD)">바레인 디나르 (AUD)</option>
              <option value="달러 (BND)">브루나이 달러 (BND)</option>
              <option value="달러 (CAD)">캐나다 달러 (CAD)</option>
              <option value="프랑 (CHF)">스위스 프랑 (CHF)</option>
              <option value="위안화 (CNH)">위안화 (CNH)</option>
              <option value="크로네 (DKK)">덴마아크 크로네 (DKK)</option>
              <option value="유로 (EUR)">유로 (EUR)</option>
              <option value="파운드 (GBP)">영국 파운드 (GBP)</option>
              <option value="달러 (HKD)">홍콩 달러 (HKD)</option>
              <option value="루피아 (IDR(100))">
                인도네시아 루피아 (IDR(100))
              </option>
              <option value="옌 (JPY(100))">일본 옌 (JPY(100))</option>
              <option value="원 (KRW)">한국 원 (KRW)</option>
              <option value="디나르 (KWD)">쿠웨이트 디나르 (KWD)</option>
              <option value="링기트 (MYR)">말레이지아 링기트 (MYR)</option>
              <option value="크로네 (NOK)">노르웨이 크로네 (NOK)</option>
              <option value="달러 (NZD)">뉴질랜드 달러 (NZD)</option>
              <option value="리얄 (SAR)">사우디 리얄 (SAR)</option>
              <option value="크로나 (SEK)">스웨덴 크로나 (SEK)</option>
              <option value="달러 (SGD)">싱가포르 달러 (SGD)</option>
              <option value="바트 (THB)">태국 바트 (THB)</option>
              <option value="달러 (USD)">미국 달러 (USD)</option>
            </select>
            <input
              type="number"
              style="border-radius: 15px;"
              class="form-control"
              placeholder="금액 입력"
              v-model="foreign_money"
              @input="f_to_k"
            />
            <span class="ms-2">{{ formatted_foreign_money }} {{ country }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";
const country = ref("");
const won = ref(0);
const foreign_money = ref(0);
const formatted_won = ref("");
const formatted_foreign_money = ref("");

function extractCurrencyCode(value) {
  const match = value.match(/\(([^)]+)\)/);
  return match ? match[1] : null;
}

// 숫자를 한국어 단위로 변환하는 함수
function formatKoreanCurrency(value) {
  // 값이 없으면 빈 문자열을 반환
  if (!value) return "";

  // 숫자를 문자열로 변환
  const numberString = value.toString();
  // 소수점 기준으로 문자열을 분리
  const parts = numberString.split(".");
  // 정수 부분과 소수 부분을 구분
  let integerPart = parts[0];
  const decimalPart = parts.length > 1 ? "." + parts[1] : "";

  // 한국어 단위를 나타내는 배열
  const units = ["", "만", "억", "조"];
  let result = "";
  let unitIndex = 0;

  // 정수 부분을 오른쪽에서부터 4자리씩 잘라서 처리
  while (integerPart.length > 0) {
    // 마지막 4자리를 잘라서 chunk에 저장
    const chunk = integerPart.slice(-4);
    // 정수 부분에서 잘라낸 부분을 제거
    integerPart = integerPart.slice(0, -4);

    // chunk가 "0000"이 아닌 경우에만 처리
    if (chunk !== "0000") {
      result =
        parseInt(chunk, 10) + // chunk를 숫자로 변환
        (units[unitIndex] ? " " + units[unitIndex] : "") + // 적절한 한국어 단위를 추가
        (result ? " " + result : ""); // 결과 문자열에 추가
    }
    // 단위 인덱스를 증가
    unitIndex++;
  }

  // 결과 문자열에 소수 부분을 추가하여 반환
  return result + decimalPart;
}



watch(won, (newVal) => {
  formatted_won.value = formatKoreanCurrency(newVal);
});

watch(foreign_money, (newVal) => {
  formatted_foreign_money.value = formatKoreanCurrency(newVal);
});


// 한국 화폐 -> 외국 화폐
const k_to_f = () => {
  if (country.value && won.value) {
    const currencyCode = extractCurrencyCode(country.value);
    console.log(currencyCode);
    axios({
      method: "get",
      url: `${API_URL}/exchange/k_to_f/${won.value}/${currencyCode}`,
    })
      .then((response) => {
        foreign_money.value = response.data.result; // 서버가 반환하는 계산된 값을 할당
      })
      .catch((error) => {
        console.log(error);
      });
  }
};

// 외국 화폐 -> 한국 화폐
const f_to_k = () => {
  if (country.value && foreign_money.value) {
    const currencyCode = extractCurrencyCode(country.value);
    console.log(currencyCode);
    axios
      .get(`${API_URL}/exchange/f_to_k/${foreign_money.value}/${currencyCode}`)
      .then((response) => {
        console.log(response);
        won.value = response.data.result; // 서버가 반환하는 계산된 값을 할당
      })
      .catch((error) => {
        console.log(error);
      });
  }
};

// 데이터가 존재하지 않을 때만 axios 요청으로 save
onMounted(() => {
  axios({
    method: "get",
    url: `${API_URL}/exchange/check`,
  })
    .then((response) => {
      if (!response.data.data_exists) {
        axios({
          method: "get",
          url: `${API_URL}/exchange/save`,
        })
          .then((response) => {
            console.log("저장완료!");
            console.log(response);
          })
          .catch((error) => {
            console.log(error);
          });
      }
    })
    .catch((error) => {
      console.log(error);
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

img {
  border-radius: 15px;
}

.form {
  width: 100%;
  padding: 10px;
}

.d-flex {
  display: flex;
  width: 100%;
  margin: 5px 0;
}

.form-select,
.form-control,
span {
  flex: 1;
  margin: 0 5px;
}

span {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.1);
  border-radius: 15px;
  height: 40px;
  padding: 5px;
}
</style>
