<template>
  <section id="contact" class="contact">
    <h2>Contacto</h2>
    <p>¿Tienes ideas o bugs para reportar? Escríbeme.</p>
    <div class="links">
      <a href="mailto:contact@dopeldev.com">contact@dopeldev.com</a>
      <a href="https://github.com/dopeldev" target="_blank" rel="noopener">
        GitHub
      </a>
      <a href="https://www.linkedin.com/in/dopeldev/" target="_blank" rel="noopener">
        LinkedIn
      </a>
    </div>
  </section>
</template>

<style scoped lang="scss">
.contact {
  padding: 48px 16px 64px;
  text-align: center;

  h2 {
    margin-bottom: 12px;
  }

  .links {
    margin-top: 16px;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 16px;

    a {
      color: var(--accent);
      font-weight: 600;
    }
  }
}
</style>

