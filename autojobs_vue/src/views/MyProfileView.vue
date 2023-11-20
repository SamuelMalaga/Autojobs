<template>
  <div class="tile is-ancestor">
  <div class="tile is-3 is-vertical is-parent">
    <div class="tile is-child box">
      <UserInfo/>
    </div>
  </div>
  <div class="tile is-parent is-vertical">
    <!-- <div class="tile is-child  box">
    </div> -->
      <WorkExperiences/>
    <!-- <div class="tile is-child  box">
    </div> -->
      <EducationalExperiences/>
      <Certifications/>
      <Languages/>
  </div>
</div>
</template>

<script>
import WorkExperiences from '@/components/WorkExperiences.vue';
import UserInfo from '@/components/UserInfo.vue';
import EducationalExperiences from '@/components/EducationalExperiences.vue';
import Certifications from '@/components/Certifications.vue';
import Languages from '@/components/Languages.vue';


export default {
  name: 'MyProfile',
  components: {
    WorkExperiences,
    UserInfo,
    EducationalExperiences,
    Certifications,
    Languages,
  },
  created() {
    // Exemplo: Se as informações do usuário não estiverem disponíveis, redirecione para outra página
    if (!this.$store.getters.getFullUserInfo) {
      this.$router.push('/'); // ou qualquer outra página
    }
  },
}
</script>
