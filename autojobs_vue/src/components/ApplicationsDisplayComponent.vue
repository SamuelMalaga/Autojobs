<template>

  <div class="column is-4  notification is-primary ">
    <p class="title">{{ColumnStatus}}</p>
    <div class="container ">
      <div v-for="application in this.ApplicationsList" :key="id">
        <div v-if="application.appl_status === this.ColumnStatus">
          <div class="card">
            <header class="card-header">
              <p class="card-header-title">
                Application At {{application.appl_job.company_name}} For {{application.appl_job.job_title}}
                ID: {{application.id}}
              </p>
              <button class="card-header-icon"  @click="toggleCard(application.id)">
                <span class="icon">
                  <a  ><font-awesome-icon  icon="angle-down"  /></a>
                </span>
              </button>
            </header>
            <div class="hidden-content" v-if="expandedCards.includes(application.id)" >
              <div class="card-content">
                <div class="content">
                  <p> Last update status: </p>
                  <div class="columns is-gapless is-multiline">
                    <div class="column ">
                      <button class="button is-fullwidth" >Generate resumé</button>
                    </div>
                    <div class="column ">
                      <button class="button is-fullwidth" >Used resumé</button>
                    </div>
                  </div>
                </div>
                <footer class="card-footer">
                  <a class="card-footer-item" @click="changeStatus(application,this.PreviousColumnStatus)" ><font-awesome-icon  icon="arrow-left"  /></a>
                  <a  class="card-footer-item" @click="saveApplicationStatus(application)"><font-awesome-icon  icon="floppy-disk" /></a>
                  <a  class="card-footer-item" @click="changeStatus(application,this.NextColumnStatus)" ><font-awesome-icon  icon="arrow-right"  /></a>
                </footer>
              </div>
            </div>
          </div>
          <div class="column is-0"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    ApplicationsList: {
      type: Array,
      required: true
    },
    ColumnStatus: String,
    NextColumnStatus:String,
    PreviousColumnStatus:String,
    toggleCard: Function,
    expandedCards:{
      type:Function,
      required:true
    },
    changeStatus:{
      type:Function,
      required:true
    },
    saveApplicationStatus:{
      type:Function,
      required:true
    },
  },
};
</script>
