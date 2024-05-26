<template>
  <div :class="{ 'dark-mode-content': darkMode}">
    <Navbar :darkMode="darkMode" @toggle-dark-mode="toggleDarkMode"></Navbar>
    <div class="registration-form is-center" :class="{ 'dark-mode-content': darkMode }">
      <form @submit.prevent="submitForm">
        <div class="field">
          <label class="label">Имя пользователя</label>
          <div class="control">
            <input class="input" type="text" v-model="form.username" placeholder="Введите имя пользователя">
          </div>
        </div>
        <div class="field">
          <label class="label">Email</label>
          <div class="control">
            <input class="input" type="email" v-model="form.email" placeholder="Введите адрес электронной почты">
          </div>
        </div>
        <div class="field">
          <label class="label">Пароль</label>
          <div class="control">
            <input class="input" type="password" v-model="form.password" placeholder="Введите пароль">
          </div>
        </div>
        <div class="field">
          <div class="control">
            <button class="button is-black is-rounded" type="submit">Зарегистрироваться</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Navbar from "../components/Navbar.vue"

export default {
  name: 'Registration',
  components: {
    Navbar
  },
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
      },
      darkMode: false,
    }
  },
  methods: {
    submitForm() {
      const formData = new FormData();
      formData.append('username', this.form.username);
      formData.append('email', this.form.email);
      formData.append('password', this.form.password);

      axios.post('/api/registration/', formData, { withCredentials: true })
        .then(response => {
          if (document.cookie.includes('access_token')) {
            this.goToBoardPage();
          } else {
            console.log('Access token not found in cookies');
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    goToBoardPage() {
      this.$router.push({ name: 'Board' });
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
    },
    toggleNavbar() {
      this.isNavbarActive = !this.isNavbarActive;
    },
  }
}
</script>

<style scoped>
.registration-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
}

.registration-form .field {
  margin-bottom: 20px;
}

.registration-form .label {
  font-weight: bold;
}

.registration-form .input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  background-color: #fff; 
  border: 1px solid #ccc;
}

.registration-form .button {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.registration-form .button:hover {
  background-color: #f0f0f0; 
}

.dark-mode-content {
  background-color: #1a1a1a; 
  color: #f0f0f0; 
  height: 690px;
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
