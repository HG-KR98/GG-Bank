import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";
import { onMounted } from "vue";

export const useFinancialStore = defineStore(
  "financial",
  () => {
    const router = useRouter();
    // django로 요청 보내는 url
    const API_URL = "http://127.0.0.1:8000";

    // 정기예금 base_list
    const depositBaseList = ref([]);

    // 정기예금 option_list
    const depositOptionList = ref([]);

    // 적금 base_list
    const savingBaseList = ref([]);

    // 적금 option_list
    const savingOptionList = ref([]);

    // 포트폴리오 list
    const portFolio = ref([]);

    // 예금 저장
    const saveDeposit = function () {
      axios({
        method: "get",
        url: `${API_URL}/financial_products/deposit_save`,
      })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    };

    // 적금 저장
    const saveSaving = function () {
      axios({
        method: "get",
        url: `${API_URL}/financial_products/saving_save`,
      })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    };
    const getDepositBaseList = function () {
      axios({
        method: "get",
        url: `${API_URL}/financial_products/deposit_base_list/`,
      })
        .then((response) => {
          depositBaseList.value = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const getDepositOptionList = function () {
      axios({
        method: "get",
        url: `${API_URL}/financial_products/deposit_option_list/`,
      })
        .then((response) => {
          depositOptionList.value = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const getSavingBaseList = function () {
      axios({
        method: "get",
        url: `${API_URL}/financial_products/saving_base_list/`,
      })
        .then((response) => {
          savingBaseList.value = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const getSavingOptionList = function () {
      axios({
        method: "get",
        url: `${API_URL}/financial_products/saving_option_list/`,
      })
        .then((response) => {
          savingOptionList.value = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    return {
      API_URL,
      depositBaseList,
      depositOptionList,
      savingBaseList,
      savingOptionList,
      saveDeposit,
      getDepositBaseList,
      getSavingBaseList,
      saveSaving,
      saveDeposit,
      getDepositOptionList,
      getSavingOptionList,
    };
  },
  { persist: true }
);
