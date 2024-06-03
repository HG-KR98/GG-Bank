<template>
  <div v-if="deposit" class="container mt-5">
    <div class="card">
      <div class="card-header text-center">
        <h1>{{ deposit.fin_prdt_nm }} 상세페이지</h1>
      </div>
      <div class="card-body d-flex flex-column">
        <ul class="list-group list-group-flush flex-grow-1">
          <li class="list-group-item flex-grow-1 d-flex align-items-center">
            <strong>공시 제출일:</strong>
            <span class="ms-2">{{ deposit.dcls_month }}</span>
          </li>
          <li class="list-group-item flex-grow-1 d-flex align-items-center">
            <strong>금융회사명:</strong>
            <span class="ms-2">{{ deposit.kor_co_nm }}</span>
          </li>
          <li class="list-group-item flex-grow-1 d-flex align-items-center">
            <strong>상품명:</strong>
            <span class="ms-2">{{ deposit.fin_prdt_nm }}</span>
          </li>
          <li class="list-group-item flex-grow-1 d-flex align-items-center">
            <strong>가입제한:</strong>
            <span class="ms-2">{{ deposit.join_deny }}</span>
          </li>
          <li class="list-group-item flex-grow-1 d-flex align-items-center">
            <strong>가입 방법:</strong>
            <span class="ms-2">{{ deposit.join_way }}</span>
          </li>
          <li class="list-group-item flex-grow-1 d-flex align-items-center">
            <strong>우대조건:</strong>
            <span class="ms-2">{{ deposit.mtrt_int }}</span>
          </li>
        </ul>
      </div>
      <div class="card-footer text-center" v-if="cstore.isLogin">
        <button
          class="btn btn-primary"
          @click="
            subscribe(
              deposit.kor_co_nm,
              deposit.fin_prdt_nm,
              deposit.fin_prdt_cd,
              deposit['12']
            )
          "
        >
          가입하기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useFinancialStore } from "@/stores/financial";
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const deposit = ref(null);
const route = useRoute();
const fstore = useFinancialStore();
const cstore = useCounterStore();
const checkPortFolio = ref(null);
const router = useRouter();

const getPortFolio = function () {
  axios({
    method: "get",
    url: `${fstore.API_URL}/financial_products/port_folio/`,
    headers: {
      Authorization: `Token ${cstore.token}`,
    },
  })
    .then((response) => {
      if (
        response.data.find(
          (item) => item.fin_prdt_cd === deposit.value.fin_prdt_cd
        )
      ) {
        checkPortFolio.value = false;
      } else {
        checkPortFolio.value = true;
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

onMounted(() => {
  deposit.value = fstore.depositBaseList.find(
    (product) => product.fin_prdt_cd === route.params.fin_prdt_cd
  );
  getPortFolio();
});

const subscribe = function (
  productCompany,
  productName,
  productCd,
  IntTweleve
) {
  if (checkPortFolio.value === true) {
    alert("가입 되었습니다! 항상 감사합니다. 고객님");
    // 포트폴리오 추가 함수
    axios({
      method: "post",
      url: `${fstore.API_URL}/financial_products/port_folio/`,
      data: {
        product_kind: "정기예금",
        kor_co_nm: productCompany,
        fin_prdt_nm: productName,
        fin_prdt_cd: productCd,
        tweleve_month: IntTweleve,
      },
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
  } else {
    alert("이미 가입된 상품입니다!");
  }
  router.go(0);
};
</script>

<style scoped>
.container {
  width: 100%;
  margin: auto;
}

.card {
  min-height: 700px;
  display: flex;
  flex-direction: column;
}

.card-body {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.list-group-item {
  display: flex;
  align-items: center;
  flex-grow: 1;
}

.ms-2 {
  margin-left: 0.5rem;
}

.card-header {
  background-color: #007bff;
  color: white;
}

.btn-primary {
  background-color: #007bff;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>
