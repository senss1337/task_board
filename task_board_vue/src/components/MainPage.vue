<template>
  <div class="Main-page" :class="{ 'dark-mode-content': darkMode }">
    <Navbar :darkMode="darkMode" @toggle-dark-mode="toggleDarkMode"></Navbar>
    <section class="hero is-fullheight">
      <div class="hero-body">
        <div class="container">
          <h1 class="title is-1 has-text-centered">Добро пожаловать в Task Board</h1>
          <p class="subtitle is-4 has-text-centered">Позвольте нам помочь вам эффективно управлять вашими задачами!</p>
        </div>
      </div>
    </section>

    <section class="section is-link">
      <div class="container">
        <div class="columns is-centered">
          <div class="column is-half">
            <div class="card">
              <div class="card-content">
                <div class="content">
                  <h2 class="title is-4">О нас</h2>
                  <p>Если у вас возникают трудности с отслеживанием задач, мы предлагаем удобное решение, которое поможет вам организовать и эффективно управлять вашими задачами.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "../components/Navbar.vue"
export default {
  name: "MainPage",
  components: {
    Navbar
  },
  data() {
    return {
      darkMode: false,
    };
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
    },
    toggleNavbar() {
      this.isNavbarActive = !this.isNavbarActive;
    },
    logout() {
      axios
        .post('/api/logout/', null, { withCredentials: true })
        .then(response => {
          console.log('logout')
          this.$router.push({name: 'Logout', params: {userType:'psychologist'}});
        })
        .catch(error => {
          console.log(error)
        })
    },
  },
  created() {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
  },
};
</script>

<style>
</style>
