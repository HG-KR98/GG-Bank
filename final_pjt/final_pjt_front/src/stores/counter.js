import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore(
  "counter",
  () => {
    const userInfo = ref([]);
    // 게시판 정보
    const userId = ref(0);
    const articles = ref([]);
    const investmentArticles = ref([]);
    const customerArticles = ref([]);
    // django로 요청 보내는 url
    const API_URL = "http://127.0.0.1:8000";
    // token 변수
    const token = ref(null);
    // 로그인 여부
    const isLogin = computed(() => {
      if (token.value === null) {
        return false;
      } else {
        return true;
      }
    });
    const router = useRouter();

    // 게시글 종류별로 글 저장
    const getArticles = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((response) => {
          articles.value = response.data.filter(
            (article) => article.category === "free"
          );
          investmentArticles.value = response.data.filter(
            (article) => article.category === "investment"
          );
          customerArticles.value = response.data.filter(
            (article) => article.category === "communication"
          );
        })
        .catch((error) => {
          console.log(error);
        });
    };

    // 자유 게시판 글 갯수
    const articlesLen = computed(() => {
      return articles.value.length;
    });

    const signUp = function (payload) {
      const {
        username,
        password1,
        password2,
        email,
        name,
        gender,
        birth_date,
        phone_number,
        assets,
      } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          password1,
          password2,
          email,
          name,
          gender,
          birth_date,
          phone_number,
          assets,
        },
      })
        .then((response) => {
          console.log("회원가입 성공!");
          const password = password1;
          logIn({ username, password });
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const logIn = function (payload) {
      const { username, password } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        data: {
          username,
          password,
        },
      })
        .then((response) => {
          token.value = response.data.key;
          userId.value = response.data.user;
          userInfo.value = response.data.user;
          console.log(response.data.user);
          router.push({ name: "home" });
        })
        .catch((error) => {
          console.log(error);
        });
    };

    return {
      articles,
      API_URL,
      getArticles,
      signUp,
      logIn,
      token,
      isLogin,
      investmentArticles,
      customerArticles,
      articlesLen,
      userId,
      userInfo,
    };
  },
  { persist: true }
);
