<template>
  <Navbar :darkMode="darkMode" @toggle-dark-mode="toggleDarkMode"></Navbar>
    <div :class="{ 'dark-mode-content': darkMode }" class="board-form">
      <form @submit.prevent="submitForm">
        <div class="field">
          <label class="label">Название</label>
          <div class="control">
            <input class="input" type="text" v-model="form.name" placeholder="Введите название">
          </div>
        </div>
        <div class="field">
          <label class="label">Автор</label>
          <div class="control">
            <input class="input" type="text" v-model="form.author" placeholder="Введите имя автора">
          </div>
        </div>
        <div class="field">
          <label class="label">Дата создания</label>
          <div class="control">
            <input class="input" type="date" v-model="form.date_created" readonly>
          </div>
        </div>
        <div class="field">
          <label class="checkbox">
            <input type="checkbox" v-model="form.is_private">
            Приватная доска
          </label>
        </div>
        <div class="field">
          <label class="label">Тема</label>
          <div class="control">
            <input class="input" type="text" v-model="form.theme" placeholder="Введите тему">
          </div>
        </div>
        <div class="field">
          <div class="control">
            <button class="button is-black" type="submit">Создать доску</button>
          </div>
        </div>
      </form>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"
export default {
  components: {
    Navbar
  },
  data() {
    return {
      form: {
        name: '',
        author: '',
        date_created: '',
        is_private: true,
        theme: '',
      },
      tasks: [],
      darkMode: false,
    };
  },
  methods: {
    submitForm() {
      console.log('Доска создана:', this.form);
      this.$router.push({ name: 'CreateTask' });
    },
    addTask() {
      this.tasks.push({ name: '', completed: false });
    },
    deleteTask(index) {
      this.tasks.splice(index, 1);
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
  },
  toggleNavbar() {
    this.isNavbarActive = !this.isNavbarActive;
  },
  },
  created() {
    this.form.date_created = new Date().toISOString().slice(0, 10);
  },
};
</script>

<style scoped>
.board-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border-radius: 5px;
  background-color: #f7f7f7; 
}

.board-form .field {
  margin-bottom: 20px;
}

.board-form .label {
  font-weight: bold;
}

.board-form .input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  background-color: #fff; 
  border: 1px solid #ccc;
}

.board-form .button {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.board-form .button:hover {
  background-color: darkgrey; 
  color: #fff;
}

.dark-mode-content {
  background-color: #1a1a1a; 
  color: #f0f0f0;
}

.dark-mode-content .label {
  color: #fff; 
}

.dark-mode-content .input {
  background-color: #333; 
  color: #fff; 
}

.dark-mode-content .button {
  background-color: #ffc107; 
  color: #333; 
}
</style>
