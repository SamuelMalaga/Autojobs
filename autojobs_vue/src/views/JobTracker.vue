<template>
  <div class="table-container">
    <div class="columns is-mobile ml-5">
      <div class="column is-4 notification is-primary  ">
        <p class="title">Screening</p>
        <div class="container ">
          <div v-for="application in applications" :key="id">
            <div v-if="application.appl_status === 'Screening'">
              <div class="card">
                <header class="card-header">
                  <p class="card-header-title">
                    Application At {{application.appl_job.company_name}} For {{application.appl_job.job_title}}
                  </p>
                  <button class="card-header-icon" @click="toggleCard(application.id)">
                    <span class="icon">
                      <a  ><font-awesome-icon  icon="angle-down"  /></a>
                    </span>
                  </button>
                </header>
                <div class="hidden-content"  v-if="expandedCards.includes(application.id)">
                  <div class="card-content">
                    <div class="content">
                      Lorem ipsum leo risus, porta ac consectetur ac, vestibulum at eros. Donec id elit non mi porta gravida at eget metus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras mattis consectetur purus sit amet fermentum.
                      <p>
                        {{ application.appl_status }}
                      </p>
                    </div>
                    <footer class="card-footer">
                      <a class="card-footer-item" @click="this.changeStatus(application,'Cancelled')"><font-awesome-icon  icon="arrow-left"  /></a>
                      <a  class="card-footer-item" @click="this.saveApplicationStatus(application)" ><font-awesome-icon  icon="floppy-disk" /></a>
                      <a  class="card-footer-item" @click="this.changeStatus(application,'Inital interview')"><font-awesome-icon  icon="arrow-right"  /></a>
                    </footer>
                  </div>
                </div>
              </div>
              <div class="column is-0"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-0"></div>
      <div class="column is-4 notification is-primary  ">
        <p class="title">Initial Interview</p>
        <div class="container ">
          <div v-for="application in applications" :key="id">
            <div v-if="application.appl_status === 'Inital interview'">
              <div class="card">
                <header class="card-header">
                  <p class="card-header-title">
                    Application At {{application.appl_job.company_name}} For {{application.appl_job.job_title}}
                    ID: {{ application.id }}
                  </p>
                  <button class="card-header-icon" @click="toggleCard(application.id)">
                    <span class="icon">
                      <a  ><font-awesome-icon  icon="angle-down"  /></a>
                    </span>
                  </button>
                </header>
                <div class="hidden-content"  v-if="expandedCards.includes(application.id)">
                  <div class="card-content">
                    <div class="content">
                      Lorem ipsum leo risus, porta ac consectetur ac, vestibulum at eros. Donec id elit non mi porta gravida at eget metus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras mattis consectetur purus sit amet fermentum.
                      <p>
                        {{ application.appl_status }}
                      </p>
                    </div>
                    <footer class="card-footer">
                      <a class="card-footer-item" @click="this.changeStatus(application,'Screening')"><font-awesome-icon  icon="arrow-left"  /></a>
                      <a  class="card-footer-item" @click="this.saveApplicationStatus(application)" ><font-awesome-icon  icon="floppy-disk" /></a>
                      <a  class="card-footer-item" @click="this.changeStatus(application,'Interview')"><font-awesome-icon  icon="arrow-right"  /></a>
                    </footer>
                  </div>
                </div>
              </div>
              <div class="column is-0"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-0"></div>
      <div class="column is-4 notification is-primary  ">
        <p class="title">Interview</p>
        <div class="container ">
          <div v-for="application in applications" :key="id">
            <div v-if="application.appl_status === 'Interview'">
              <div class="card">
                <header class="card-header">
                  <p class="card-header-title">
                    Application At {{application.appl_job.company_name}} For {{application.appl_job.job_title}}
                  </p>
                  <button class="card-header-icon" @click="toggleCard(application.id)">
                    <span class="icon">
                      <a  ><font-awesome-icon  icon="angle-down"  /></a>
                    </span>
                  </button>
                </header>
                <div class="hidden-content"  v-if="expandedCards.includes(application.id)">
                  <div class="card-content">
                    <div class="content">
                      Lorem ipsum leo risus, porta ac consectetur ac, vestibulum at eros. Donec id elit non mi porta gravida at eget metus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras mattis consectetur purus sit amet fermentum.
                      <p>
                        {{ application.appl_status }}
                      </p>
                    </div>
                    <footer class="card-footer">
                      <a class="card-footer-item" @click="this.changeStatus(application,'Initial Interview')"><font-awesome-icon  icon="arrow-left"  /></a>
                      <a href="#" class="card-footer-item" aria-disabled="true"></a>
                      <a  class="card-footer-item" @click="this.changeStatus(application,'Technical Interview')"><font-awesome-icon  icon="arrow-right"  /></a>
                    </footer>
                  </div>
                </div>
              </div>
              <div class="column is-0"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-0"></div>
      <div class="column is-4  notification is-primary  ">
        <p class="title">Technical Interview</p>
        <div class="container ">
          <div v-for="application in applications" :key="id">
            <div v-if="application.appl_status === 'Technical Interview'">
              <div class="card">
                <header class="card-header">
                  <p class="card-header-title">
                    Application At {{application.appl_job.company_name}} For {{application.appl_job.job_title}}
                  </p>
                  <button class="card-header-icon" @click="toggleCard(application.id)">
                    <span class="icon">
                      <a  ><font-awesome-icon  icon="angle-down"  /></a>
                    </span>
                  </button>
                </header>
                <div class="hidden-content"  v-if="expandedCards.includes(application.id)">
                  <div class="card-content">
                    <div class="content">
                      Lorem ipsum leo risus, porta ac consectetur ac, vestibulum at eros. Donec id elit non mi porta gravida at eget metus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras mattis consectetur purus sit amet fermentum.
                      <p>
                        {{ application.appl_status }}
                      </p>
                    </div>
                    <footer class="card-footer">
                      <a class="card-footer-item" @click="this.changeStatus(application,'Interview')"><font-awesome-icon  icon="arrow-left"  /></a>
                      <a href="#" class="card-footer-item" aria-disabled="true"></a>
                      <a  class="card-footer-item" @click="this.changeStatus(application,'Technical Assessment')"><font-awesome-icon  icon="arrow-right"  /></a>
                    </footer>
                  </div>
                </div>
              </div>
              <div class="column is-0"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-0"></div>
      <div class="column is-4  notification is-primary  ">
        <p class="title">Technical Assessment</p>
        <div class="container ">
          <div v-for="application in applications" :key="id">
            <div v-if="application.appl_status === 'Technical Assessment'">
              <div class="card">
                <header class="card-header">
                  <p class="card-header-title">
                    Application At {{application.appl_job.company_name}} For {{application.appl_job.job_title}}
                  </p>
                  <button class="card-header-icon" @click="toggleCard(application.id)">
                    <span class="icon">
                      <a  ><font-awesome-icon  icon="angle-down"  /></a>
                    </span>
                  </button>
                </header>
                <div class="hidden-content"  v-if="expandedCards.includes(application.id)">
                  <div class="card-content">
                    <div class="content">
                      Lorem ipsum leo risus, porta ac consectetur ac, vestibulum at eros. Donec id elit non mi porta gravida at eget metus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras mattis consectetur purus sit amet fermentum.
                      <p>
                        {{ application.appl_status }}
                      </p>
                    </div>
                    <footer class="card-footer">
                      <a class="card-footer-item" @click="this.changeStatus(application,'Technical Interview')"><font-awesome-icon  icon="arrow-left"  /></a>
                      <a href="#" class="card-footer-item" aria-disabled="true"></a>
                      <a  class="card-footer-item" @click="this.changeStatus(application,'Proposal')"><font-awesome-icon  icon="arrow-right"  /></a>
                    </footer>
                  </div>
                </div>
              </div>
              <div class="column is-0"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-0"></div>
      <div class="column is-4  notification is-primary  ">
        <p class="title">Proposal</p>
        <div class="container ">
          <div v-for="application in applications" :key="id">
            <div v-if="application.appl_status === 'Proposal'">
              <div class="card">
                <header class="card-header">
                  <p class="card-header-title">
                    Application At {{application.appl_job.company_name}} For {{application.appl_job.job_title}}
                  </p>
                  <button class="card-header-icon" @click="toggleCard(application.id)">
                    <span class="icon">
                      <a  ><font-awesome-icon  icon="angle-down"  /></a>
                    </span>
                  </button>
                </header>
                <div class="hidden-content"  v-if="expandedCards.includes(application.id)">
                  <div class="card-content">
                    <div class="content">
                      Lorem ipsum leo risus, porta ac consectetur ac, vestibulum at eros. Donec id elit non mi porta gravida at eget metus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras mattis consectetur purus sit amet fermentum.
                      <p>
                        {{ application.appl_status }}
                      </p>
                    </div>
                    <footer class="card-footer">
                      <a class="card-footer-item" @click="this.changeStatus(application,'Technical Assessment')"><font-awesome-icon  icon="arrow-left"  /></a>
                      <a href="#" class="card-footer-item" aria-disabled="true"></a>
                      <a  class="card-footer-item" @click="this.changeStatus(application,'Cancelled')"><font-awesome-icon  icon="arrow-right"  /></a>
                    </footer>
                  </div>
                </div>
              </div>
              <div class="column is-0"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-0"></div>
      <div class="column is-4  notification is-primary  ">
        <p class="title">Cancelled</p>
        <div class="container ">
          <div v-for="application in applications" :key="id">
            <div v-if="application.appl_status === 'Cancelled'">
              <div class="card">
                <header class="card-header">
                  <p class="card-header-title">
                    Application At {{application.appl_job.company_name}} For {{application.appl_job.job_title}}
                  </p>
                  <button class="card-header-icon" @click="toggleCard(application.id)">
                    <span class="icon">
                      <a  ><font-awesome-icon  icon="angle-down"  /></a>
                    </span>
                  </button>
                </header>
                <div class="hidden-content"  v-if="expandedCards.includes(application.id)">
                  <div class="card-content">
                    <div class="content">
                      Lorem ipsum leo risus, porta ac consectetur ac, vestibulum at eros. Donec id elit non mi porta gravida at eget metus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras mattis consectetur purus sit amet fermentum.
                      <p>
                        {{ application.appl_status }}
                      </p>
                    </div>
                    <footer class="card-footer">
                      <a class="card-footer-item" @click="this.changeStatus(application,'Proposal')"><font-awesome-icon  icon="arrow-left"  /></a>
                      <a href="#" class="card-footer-item" aria-disabled="true"></a>
                      <a  class="card-footer-item" @click="this.changeStatus(application,'Screening')"><font-awesome-icon  icon="arrow-right"  /></a>
                    </footer>
                  </div>
                </div>
              </div>
              <div class="column is-0"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-0"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'JobTracker',
  components: {
  },
  data(){
    return{
      expandedCards: [],
      applications:[],
      status_options:[],
      screeningApplications:[],
      initialInterviewApplications:[],
      interviewApplications:[],
      technicalInterviewApplications:[],
      technicalAssessmentApplications:[],
      proposalApplications:[],
      cancelledApplications:[]
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
    sortApplications(fetchedApplications){
      for (const application of fetchedApplications) {
        switch(application.appl_status){
          case 'Screening':
            this.screeningApplications.push(application)
            break;
          case 'Interview':
            this.initialInterviewApplications.push(application)
            break;
          case 'Technical Interview':
            this.interviewApplications.push(application)
            break;
          case 'Inital interview':
            this.technicalInterviewApplications.push(application)
            break;
          case 'Techincal Assessment':
            this.technicalAssessmentApplications.push(application)
            break;
          case 'Proposal':
            this.proposalApplications.push(application)
            break;
          case 'Cancelled':
            this.cancelledApplications.push(application)
            break;
        }
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
        this.sortApplications(this.applications)
        console.log('Screening',this.screeningApplications)
        console.log('Cancelled',this.cancelledApplications)
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
    }
  },
  created(){
    this.fetchApplications(`http://127.0.0.1:8000/users/${this.$store.getters.getUserId}/applications/`)
  }


}
</script>
