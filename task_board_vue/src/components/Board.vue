<template>
  <Navbar :darkMode="darkMode" @toggle-dark-mode="toggleDarkMode"></Navbar>
  <div class="container" :class="{ 'dark-mode-content': darkMode}">
    <h1 class="title">Доски</h1>
    <button class="button is-black text-white" @click="createBoard">Создать доску</button>
    <div v-if="boards.length === 0">
      <p>У вас пока нет досок.</p>
    </div>
    <div v-else>
      <div class="columns is-multiline">
        <div class="column is-one-third" v-for="board in boards" :key="board.id">
          <div class="card">
            <div class="card-content">
              <p class="title">{{ board.name }}</p>
              <p class="subtitle">{{ board.theme }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"
export default {
  data() {
    return {
      boards: [], 
      darkMode: false
    };
  },
  components: {
    Navbar
  },
  methods: {
    createBoard() {
      this.$router.push({ name: 'CreateBoard' });
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
    },
    toggleNavbar() {
      this.isNavbarActive = !this.isNavbarActive;
    },
  },
};
</script>

<style scoped>
.container {
  
  padding: 0 20px;
  width: 2000px;
  height: 670px;
}

.title {
  font-size: 24px;
  margin-bottom: 20px;
}

.button {
  margin-bottom: 20px;
}

.card {
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
}

.card-content {
  padding: 20px;
}

.title, .subtitle {
  margin-bottom: 5px;
}
</style>
