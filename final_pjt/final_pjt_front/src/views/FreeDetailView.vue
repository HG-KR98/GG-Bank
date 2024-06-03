<template>
  <div v-if="article" class="main-container">
    <div class="article-detail-container">
      <!-- 상단 -->
      <div class="card article-card">
        <!-- 글 제목 및 버튼(좋아요, 수정, 뒤로가기) -->
        <h1 class="card-header d-flex justify-content-between">
          {{ article.title }}
          <div class="d-flex">
            <div v-if="store.userInfo.id === article?.user.id" class="me-2">
              <button
                @click="deleteArticle(article.user.id, article.id)"
                class="btn btn-delete me-2"
              >
                삭제
              </button>
              <button class="btn btn-update">
                <RouterLink
                  :to="{
                    name: 'UpdateArticle',
                    params: { id: article.id, category: article.category },
                  }"
                  style="text-decoration: none; color: inherit"
                  >수정</RouterLink
                >
              </button>
            </div>
            <button class="btn btn-back" @click="goBack">뒤로가기</button>
          </div>
        </h1>
        <div class="card-body">
          <p class="card-text">
            {{ article.content }}
          </p>
        </div>
      </div>

      <!-- 하단 -->
      <div class="card comment-section">
        <div class="card-header">
          <h4>댓글</h4>
        </div>
        <div class="card-body">
          <textarea
            class="form-control mb-3"
            v-model="content"
            rows="3"
            placeholder="주제와 무관한 댓글이나 악플은 경고 조치 없이 삭제되며 징계 대상이 될 수 있습니다."
            required
          ></textarea>
          <button
            class="btn btn-delete mb-3"
            @click="createComment(article.id)"
          >
            등록
          </button>
          <div v-if="comments && comments.length > 0">
            <ul class="list-group list-group-flush">
              <li
                v-for="comment in comments"
                :key="comment.id"
                class="list-group-item"
              >
                <div class="d-flex justify-content-between align-items-center">
                  <strong>{{ comment.user.username }}</strong>
                  <small>{{ formatDate(comment.created_at) }}</small>
                </div>
                <p>{{ comment.content }}</p>
                <div
                  v-if="store.userId.pk === comment.user.id"
                  class="text-end"
                >
                  <button
                    @click="deleteComment(comment.id, comment.user.id)"
                    class="btn btn-delete btn-sm"
                  >
                    삭제
                  </button>
                </div>
              </li>
            </ul>
          </div>
          <div v-else>
            <p>댓글이 없습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute, useRouter } from "vue-router";

const store = useCounterStore();
const route = useRoute();
const article = ref(null);
const likes = ref(0);
const isLiked = ref(false);
const comments = ref([]);
const content = ref("");
const router = useRouter();

const goBack = () => {
  router.go(-1);
};

const deleteArticle = (articleCreateUser, articlePk) => {
  if (store.userId.id !== articleCreateUser) {
    alert("본인의 글만 삭제할 수 있습니다!");
    return;
  } else {
    axios({
      method: "delete",
      url: `${store.API_URL}/api/v1/articles/detail/${articlePk}/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    })
      .then((response) => {
        console.log(response.data);
        router.push({ name: "ArticleView" });
      })
      .catch((error) => {
        console.log(error);
      });
  }
};

const updateArticle = (articleCreateUser, articlePk) => {
  if (store.userId.pk !== articleCreateUser) {
    alert("본인의 글만 수정할 수 있습니다!");
    return;
  }

  router.push({ name: "UpdateArticle", params: { id: articlePk } });
};

const deleteComment = (commentId, commentUserId) => {
  if (store.userId.pk !== commentUserId) {
    alert("본인의 댓글만 삭제할 수 있습니다!");
    return;
  }

  axios({
    method: "delete",
    url: `${store.API_URL}/api/v1/articles/comments/${commentId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response.data);
      comments.value = comments.value.filter(
        (comment) => comment.id !== commentId
      );
    })
    .catch((error) => {
      console.log(error);
    });
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString(); // 또는 원하는 형식으로 날짜를 포맷할 수 있습니다.
};

const createComment = (articleId) => {
  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/articles/${articleId}/comments/`,
    data: {
      content: content.value,
    },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response.data);
      comments.value.push(response.data);
      content.value = "";
    })
    .catch((error) => {
      console.log(error);
    });
};

onMounted(() => {
  // 글 가져오기
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/articles/detail/${route.params.id}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      article.value = response.data;
      isLiked.value = response.data.is_liked;
    })
    .catch((error) => {
      console.log(error);
    });

  // 댓글 목록 가져오기
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/comments/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      comments.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
  console.log(article.value);
});
</script>

<style scoped>
.main-container {
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.article-detail-container {
  width: 100%;
  max-width: 800px;
}

.card {
  border-radius: 15px;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: rgb(203, 230, 253);
  border-bottom: 1px solid #cfe7f0;
  border-radius: 15px 15px 0 0;
  padding: 20px;
  font-size: 1.5em;
}

.card-body {
  padding: 20px;
}

.card-text {
  margin-bottom: 20px;
}

.comment-section {
  margin-top: 30px;
}

.comment-section .card-header {
  background-color: rgb(203, 230, 253);
  border-bottom: 1px solid #cfe7f0;
  border-radius: 15px 15px 0 0;
}

.comment-section .card-body {
  padding: 20px;
}

textarea::placeholder {
  color: rgba(0, 0, 0, 0.5);
}

.list-group-item {
  border: none;
  border-bottom: 1px solid #cfe7f0;
  padding: 10px 15px;
}

.list-group-item:last-child {
  border-bottom: none;
}

.btn {
  border-radius: 15px;
  font-weight: bold;
  font-size: 14px;
  padding: 10px 20px;
  color: white;
}

.btn-like {
  background-color: #87cef2;
  border: none;
}

.btn-like:hover {
  background-color: #81c8e4;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}

.btn-delete {
  background-color: #c6e893;
  border: none;
}
.btn-delete:hover {
  background-color: #90f96d;
  transform: scale(1.1); /* 호버 시 약간 확대 */
  color: white;
}

.btn-update {
  background-color: #e8e47f;
  border: none;
}

.btn-update:hover {
  background-color: #ffdd7f;
  color: white;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}

.btn-back {
  background-color: #85caff;
  border: none;
}

.btn-back:hover {
  background-color: #6497fc;
  color: white;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}
</style>
