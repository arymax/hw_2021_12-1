import router from "./router.js";

const app = new Vue({
  router,
  data: () => ({
    show_menu: false,
    menu: [
      {
        type: "inner-link",
        name: "Dashboard",
        target: "/",
      },
      {
        type: "inner-link",
        name: "About",
        target: "/about",
      },
    ],
  }),
  methods: {
    go(path) {
      if (this.isCurrent(path)) return;
      this.show_menu = false;
      this.$router.push(path);
    },
    isCurrent(path) {
      if (path === this.$route.path) return true;
      else return false;
    },
  },
}).$mount("#app");
