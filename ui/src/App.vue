<template lang="pug">
  div#app
    router-view
</template>

<script>
export default {
  name: 'App',
  mounted() {
    this.init()
  },
  methods: {
    init() {}
  }
}
</script>
