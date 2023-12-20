<template>
  <nav class="panel p-1">
    <p class="panel-heading">
      My Applications
    </p>
    <div class="table-container mt-3">
      <div class="columns is-mobile ml-5">
        <ApplicationsDisplayComponent
            :ApplicationsList="applications"
            :ColumnStatus= "'Screening'"
            :NextColumnStatus="'Initial Interview'"
            :PreviousColumnStatus="'Cancelled'"
            :toggleCard="toggleCard"
            :expandedCards="expandedCards"
            :changeStatus="changeStatus"
            :saveApplicationStatus="saveApplicationStatus"
            />
        <div class="column is-0"></div>
        <ApplicationsDisplayComponent
            :ApplicationsList="applications"
            :ColumnStatus= "'Initial Interview'"
            :NextColumnStatus="'Interview'"
            :PreviousColumnStatus="'Screening'"
            :toggleCard="toggleCard"
            :expandedCards="expandedCards"
            :changeStatus="changeStatus"
            :saveApplicationStatus="saveApplicationStatus"
            />
        <div class="column is-0"></div>
          <ApplicationsDisplayComponent
            :ApplicationsList="applications"
            :ColumnStatus= "'Interview'"
            :NextColumnStatus="'Technical Interview'"
            :PreviousColumnStatus="'Initial Interview'"
            :toggleCard="toggleCard"
            :expandedCards="expandedCards"
            :changeStatus="changeStatus"
            :saveApplicationStatus="saveApplicationStatus"
            />
        <div class="column is-0"></div>
          <ApplicationsDisplayComponent
          :ApplicationsList="applications"
          :ColumnStatus= "'Technical Interview'"
          :NextColumnStatus="'Techincal Assessment'"
          :PreviousColumnStatus="'Interview'"
          :toggleCard="toggleCard"
          :expandedCards="expandedCards"
          :changeStatus="changeStatus"
          :saveApplicationStatus="saveApplicationStatus"
          />
        <div class="column is-0"></div>
        <ApplicationsDisplayComponent
          :ApplicationsList="applications"
          :ColumnStatus= "'Techincal Assessment'"
          :NextColumnStatus="'Proposal'"
          :PreviousColumnStatus="'Technical Interview'"
          :toggleCard="toggleCard"
          :expandedCards="expandedCards"
          :changeStatus="changeStatus"
          :saveApplicationStatus="saveApplicationStatus"
          />
        <div class="column is-0"></div>
        <ApplicationsDisplayComponent
          :ApplicationsList="applications"
          :ColumnStatus= "'Proposal'"
          :NextColumnStatus="'Cancelled'"
          :PreviousColumnStatus="'Techincal Assessment'"
          :toggleCard="toggleCard"
          :expandedCards="expandedCards"
          :changeStatus="changeStatus"
          :saveApplicationStatus="saveApplicationStatus"
          />
        <div class="column is-0"></div>
        <ApplicationsDisplayComponent
          :ApplicationsList="applications"
          :ColumnStatus= "'Cancelled'"
          :NextColumnStatus="'Screening'"
          :PreviousColumnStatus="'Proposal'"
          :toggleCard="toggleCard"
          :expandedCards="expandedCards"
          :changeStatus="changeStatus"
          :saveApplicationStatus="saveApplicationStatus"
          />
        <div class="column is-0"></div>
      </div>
    </div>
    <div class="panel-block">
      <p class="control has-icons-middle">
        <a class="pagination-previous" @click="showCreateApplicationAndJobModal">Create application</a>
        <CreateApplicationAndJobModal
        v-if="isCreateApplicationModalAndJobVisible"
        @close="closeCreateApplicationAndJobModal"/>
      </p>
    </div>
  </nav>
</template>

<script>
import axios from 'axios';
import ApplicationsDisplayComponent from '@/components/ApplicationsDisplayComponent.vue';
import CreateApplicationAndJobModal from '@/components/ModalComponents/ApplicationModals/CreateApplicationAndJobModal.vue'
export default {
  name: 'JobTracker',
  components: {
    ApplicationsDisplayComponent,
    CreateApplicationAndJobModal

  },
  data(){
    return{
      expandedCards: [],
      applications:[],
      isCreateApplicationModalAndJobVisible:false,

    }
  },
  created() {
    // Exemplo: Se as informações do usuário não estiverem disponíveis, redirecione para outra página
    if (!this.$store.getters.isLoggedIn) {
      this.$router.push('/'); // ou qualquer outra página
    }
  },
  methods:{
    toggleCard(applicationId) {
      const index = this.expandedCards.indexOf(applicationId);
      if (index === -1) {
        this.expandedCards.push(applicationId);
      } else {
        this.expandedCards.splice(index, 1);
      }
    },
    changeStatus(application,targetStatus){
      application.appl_status = targetStatus

      console.log(application)
    },
    async fetchApplications(url){
      try {
        const headers = {
          Authorization: `Token ${localStorage.getItem('token')}`,
        };
        const response = await axios.get(url,{headers});
        this.applications = response.data.applications;
        this.status_options = response.data.status_options;
        //this.sortApplications(this.applications)
        console.log('Technical Interview',this.technicalInterviewApplications)
      } catch (error) {
        console.error('Erro ao buscar applications:', error);
      }
    },
    async saveApplicationStatus(application){
      try {
        const headers = {
          Authorization: `Token ${localStorage.getItem('token')}`,
        };
        const body = {
            "appl_status":application.appl_status,
        };
        const updateStatusURL = `http://127.0.0.1:8000/users/${this.$store.getters.getUserId}/applications/${application.id}/update`

        console.log(updateStatusURL)
        const response = await axios.put(updateStatusURL,body,{headers});
        console.log('salvo com sucesso')
      } catch (error) {

      }
    },
    showCreateApplicationAndJobModal() {
      this.isCreateApplicationModalAndJobVisible = true;
    },
    closeCreateApplicationAndJobModal() {
      this.isCreateApplicationModalAndJobVisible = false;
    },
  },
  created(){
    this.fetchApplications(`http://127.0.0.1:8000/users/${this.$store.getters.getUserId}/applications/`)
  }


}
</script>
