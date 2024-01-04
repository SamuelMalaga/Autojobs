<template>
  <div v-if="isOpen" class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Update user Info new Modal</p>
          <button class="delete" aria-label="close" @click="handleClose"></button>
        </header>
        <section class="modal-card-body">
          <LongTextInputComponent ref="userBio" title="User Bio" placeholder="Type the name of the Institution" :default-value="UserInfo.bio"/>
          <div class="field has-addons">
            <TextInputComponent class="control is-expanded" ref="userCity" title="City" placeholder="Type the name/title of the education/course" :default-value="UserInfo.city"/>
            <TextInputComponent ref="userCountry" title="Country" placeholder="Description of your experience" :default-value="UserInfo.country"/>

          </div>
          <!-- <DropdownInputComponent ref="lngProficiencyLevel" title="Language Proficiency Level" :options="languageProficiencyOptions" /> -->
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success" @click="handleSubmit">Save changes</button>
          <button class="button" @click="handleClose">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';
import TextInputComponent from '../../CommonComponents/TextInputComponent.vue';
import DropdownInputComponent from '../../CommonComponents/DropdownInputComponent.vue'
import LongTextInputComponent from '@/components/CommonComponents/LongTextInputComponent.vue';

export default {
  components: {
    TextInputComponent,
    DropdownInputComponent,
    LongTextInputComponent
},
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    updateUrl: {
      type: String,
      required: true,
    },
    UserInfo: {
      type: Object,
      required:true
    }

  },
  data() {
    return {
      dadosEditados: {},
      languageProficiencyOptions:[
      { field_name: "Basic", field_value: "A1" },
      { field_name: "Intermediate", field_value: "B1" },
      { field_name: "Advanced", field_value: "C1" },
    ]
    };
  },
  methods: {
    handleSubmit() {
      // Chame o método para enviar a solicitação de atualização
      this.sendUpdateRequest();
      // Emitir evento para o componente pai com os dados editados
      this.$emit("submit", this.dadosEditados);

    },
    handleClose() {
      this.$emit("close");
    },
    sendUpdateRequest() {
      //const userId = this.$store.getters.getUserId;
      const updateUserInfoUrl = `${this.updateUrl}/update`
      const requestBody = {
        //Add more fields as needed
        "bio": this.$refs.userBio.getValue(),
        "country": this.$refs.userCountry.getValue(),
        "city": this.$refs.userCity.getValue()

      };
      const headers = {
        Authorization: `Token ${localStorage.getItem('token')}`,
      };
      console.log(requestBody)
      axios.put(updateUserInfoUrl, requestBody, { headers })
        .then(response => {
          this.$store.dispatch('updatePartialUserInfo',
            { bio: requestBody.bio,
              country: requestBody.country,
              city: requestBody.city,
            });
          this.$emit("data-updated");
        })
        .catch(error => {
          console.error('Erro ao atualizar dados:', error);
        });
    },

  },
};
</script>

<style lang="scss" scoped>
.popup{
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 99;
  background-color: rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;

}
</style>
