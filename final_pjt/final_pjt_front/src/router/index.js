import { createRouter, createWebHistory } from "vue-router";
import ArticleView from "@/views/ArticleView.vue";
import FreeDetailView from "@/views/FreeDetailView.vue";
import CreateView from "@/views/CreateView.vue";
import SignUpView from "@/views/SignUpView.vue";
import LogInView from "@/views/LogInView.vue";
import MyPageView from "@/views/MyPageView.vue";
import HomeView from "@/views/HomeView.vue";
import ExchangeRateView from "@/views/ExchangeRateView.vue";
import FindBankView from "@/views/FindBankView.vue";
import FreeArticlesView from "@/views/FreeArticlesView.vue";
import InvestmentArticlesView from "@/views/InvestmentArticlesView.vue";
import CustomerArticlesView from "@/views/CustomerArticlesView.vue";
import CreateInvestmentView from "@/views/CreateInvestmentView.vue";
import InvestmentDetailView from "@/views/InvestmentDetailView.vue";
import CreateCustomerView from "@/views/CreateCustomerView.vue";
import CustomerDetailView from "@/views/CustomerDetailView.vue";
import DepositListView from "@/views/DepositListView.vue";
import SavingListView from "@/views/SavingListView.vue";
import DepositDetailView from "@/views/DepositDetailView.vue";
import SavingDetailView from "@/views/SavingDetailView.vue";
import AlgorithmView from "@/views/AlgorithmView.vue";
import UpdateMyInfoView from "@/views/UpdateMyInfoView.vue";
import UpdateArticleView from "@/views/UpdateArticleView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 메인 페이지
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    // 게시판 페이지
    {
      path: "/community",
      name: "ArticleView",
      component: ArticleView,
    },
    // 자유게시판 글 생성 페이지
    {
      path: "/article_create",
      name: "CreateView",
      component: CreateView,
    },
    // 게시판 글 수정 페이지
    {
      path: "/article_update/:id/:category",
      name: "UpdateArticle",
      component: UpdateArticleView,
    },
    // 재테크 정보 공유 글 생성 페이지
    {
      path: "/investment_create",
      name: "CreateInvestment",
      component: CreateInvestmentView,
    },
    // 고객과의 소통 글 생성 페이지
    {
      path: "/customer_create",
      name: "CreateCustomer",
      component: CreateCustomerView,
    },
    // 회원 가입 페이지
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
    },
    // 개인 정보 수정 페이지
    {
      path: "/updatemyinfo",
      name: "UpdateMyInfoView",
      component: UpdateMyInfoView,
    },
    // 로그인 페이지
    {
      path: "/login",
      name: "LogInView",
      component: LogInView,
    },
    // 프로필 페이지
    {
      path: "/mypage",
      name: "MyPageView",
      component: MyPageView,
    },
    // 정기예금 비교 페이지
    {
      path: "/depositList",
      name: "DepositListView",
      component: DepositListView,
    },
    // 정기예금 상세페이지
    {
      path: "/depositList/:fin_prdt_cd",
      name: "DepositDetailView",
      component: DepositDetailView,
    },
    // 정기적금 비교 페이지
    {
      path: "/savingListView",
      name: "SavingListView",
      component: SavingListView,
    },
    // 정기적금 상세 페이지
    {
      path: "/savingList/:fin_prdt_cd",
      name: "SavingDetailView",
      component: SavingDetailView,
    },
    // 환율 계산 페이지
    {
      path: "/exchangerate",
      name: "ExchangeRateView",
      component: ExchangeRateView,
    },
    // 근처 은행 검색 페이지
    {
      path: "/findbank",
      name: "FindBankView",
      component: FindBankView,
    },
    // 자유게시판 글 목록 페이지
    {
      path: "/articles",
      name: "FreeArticlesView",
      component: FreeArticlesView,
    },
    // 자유게시판 상세 페이지
    {
      path: "/articles/:id",
      name: "FreeDetailView",
      component: FreeDetailView,
      beforeEnter: (to, from) => {
        increaseViewCount(to.params.id);
      },
    },
    // 재테크 정보 공유 글 목록 페이지
    {
      path: "/investmentarticles",
      name: "InvestmentArticlesView",
      component: InvestmentArticlesView,
    },
    // 재테크 정보 공유 상세 페이지
    {
      path: "/investmentarticles/:id",
      name: "InvestmentDetailView",
      component: InvestmentDetailView,
    },
    // 고객과의 소통 글 목록 페이지
    {
      path: "/CustomerArticles",
      name: "CustomerArticlesView",
      component: CustomerArticlesView,
    },
    // 고객과의 소통 상세 페이지
    {
      path: "/CustomerArticles/:id",
      name: "CustomerDetailView",
      component: CustomerDetailView,
    },
    // 알고리즘 추천 페이지
    {
      path: "/algorithm",
      name: "AlgorithmView",
      component: AlgorithmView,
    },
  ],
});

import { useCounterStore } from "@/stores/counter";
import axios from "axios";

router.beforeEach((to, from) => {
  const store = useCounterStore();
  // 인증되지 않은 사용자는 메인 페이지에 접근 할 수 없음
  if (to.name === "ArticleView" && store.isLogin === false) {
    // if ((to.name === "ArticleView" || to.name === "MyPageView") && store.isLogin === false) {
    window.alert("로그인해 주세요");
    return { name: "LogInView" };
  }

  // 인증된 사용자는 회원가입과 로그인 페이지에 접근 할 수 없음
  if (
    (to.name === "SignUpView" || to.name === "LogInView") &&
    store.isLogin === true
  ) {
    window.alert("이미 로그인 했습니다.");
    return { name: "ArticleView" };
  }
});

// 조회수 증가 메서드
function increaseViewCount(articleId) {
  const store = useCounterStore();
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/article_increase_views/${articleId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log("조회수 증가 성공:", response.data);
    })
    .catch((error) => {
      console.error("조회수 증가 실패:", error);
    });
}

export default router;
