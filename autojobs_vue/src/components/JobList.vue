<template>
    <div class="container">
      <div class="container">
        <nav class="panel">
          <p class="panel-heading">
            Jobs
          </p>
          <div class="panel-block">
            <p class="control has-icons-left">
              <input class="input" type="text" placeholder="Search">
              <span class="icon is-left">
                <i class="fas fa-search" aria-hidden="true"></i>
              </span>
            </p>
            <a class="pagination-previous"  @click="showModal">Add job</a>
            <a class="pagination-previous" >Run scraper</a>
            <ExecuteBotModal v-if="isModalVisible" @close="closeModal" />
          </div>
          <div class="container p-2">
            <div  v-for="job in jobs" :key="job.id" class="p-2">
              <div class="card">
              <header class="card-header">
                <p class="card-header-title">
                  {{job.job_title}} at {{job.company_name}}
                </p>
                <button class="card-header-icon" aria-label="more options" @click="toggleCard(job.id)">
                  <span class="icon">
                    <font-awesome-icon  icon="angle-down"  />
                  </span>
                </button>
              </header>
              <div class="card-content" v-if="expandedCards.includes(job.id)" >
                <div class="content">
                  <h3>Job Description</h3>
                  <div v-html="job.job_description">
                  </div>
                  <!-- <p >{{ job.job_description }}</p> -->
                  <a  @click="openJobLink(job.job_link)">Job Link</a>
                </div>
              </div>
            </div>
            </div>

          </div>
          <div class="panel-block">
            <nav class="pagination is-centered" role="navigation" aria-label="pagination">
              <a class="pagination-previous"  @click="fetchJobs(previousPageUrl)">Previous</a>

              <a class="pagination-next" @click="fetchJobs(nextPageUrl)">Next page</a>
              <!-- <ul class="pagination-list">
                <li v-if="currentPage >= 3">
                  <a class="pagination-link" aria-label="Goto page 1" @click="fetchJobs(`http://127.0.0.1:8000/jobs/?page=1`)">1</a>
                </li>
                <li >
                  <span class="pagination-ellipsis">&hellip;</span>
                </li>
                <li>
                  <a class="pagination-link" aria-label="current_page">{{ this.currentPage }}</a>
                </li>
                <li>
                  <span class="pagination-ellipsis">&hellip;</span>
                </li>
                <li v-if="currentPage < totalPages">
                  <a class="pagination-link" aria-label="Goto page {{ totalPages }}" @click="fetchJobs(`http://127.0.0.1:8000/jobs/?page=${totalPages}`)">
                    {{ totalPages }}
                  </a>
                </li>
              </ul> -->
            </nav>
          </div>
        </nav>
      </div>
    </div>
</template>

<script>
import axios from 'axios';
import ExecuteBotModal from './ExecuteBotModal.vue';


export default {
  components: {
    ExecuteBotModal,
  },
  data() {
    return {
      isModalVisible: false,
      jobs: [],
      expandedCards: [],
      nextPageUrl: null,
      previousPageUrl: null,
      currentPage: 1,
      totalPages:0,
      previousPage:0,
      nextPage:2,
      itemsPerPage: 25,
      totalItems: 0,
    };
  },
  methods: {
    async fetchJobs(url) {
      try {
        const response = await axios.get(url);
        this.jobs = response.data.results;
        this.nextPageUrl = response.data.next;
        this.previousPageUrl = response.data.previous;
        // Atualize a página atual com base na URL
        this.totalItems = response.data.count;
        this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
        const pageQueryParam = new URLSearchParams(new URL(url).search).get('page');
        this.currentPage = pageQueryParam ? parseInt(pageQueryParam, 9) : 1;
      } catch (error) {
        console.error('Erro ao buscar trabalhos:', error);
      }
    },
    toggleCard(jobId) {
      const index = this.expandedCards.indexOf(jobId);
      if (index === -1) {
        this.expandedCards.push(jobId);
      } else {
        this.expandedCards.splice(index, 1);
      }
    },
    getPaginationRange() {
      const totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
      const visiblePages = 5; // 2 anteriores, 2 posteriores, 1 current

      let startPage = Math.max(1, this.currentPage - Math.floor(visiblePages / 2));
      let endPage = Math.min(startPage + visiblePages - 1, totalPages);

      if (endPage - startPage + 1 < visiblePages) {
        startPage = Math.max(1, endPage - visiblePages + 1);
      }


      const paginationRange = [];
      if (startPage > 1) {
        paginationRange.push(1);
        if (startPage > 2) {
          paginationRange.push('ellipsis');
        }
      }

      for (let page = startPage; page <= endPage; page++) {
        paginationRange.push(page);
      }

      if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
          paginationRange.push('ellipsis');
        }
        paginationRange.push(totalPages);
      }

      return paginationRange;
    },
    openJobLink(jobLink) {
        window.open(jobLink, '_blank');
    },
    showModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
  },
  mounted() {
    this.fetchJobs('http://127.0.0.1:8000/jobs/');
  }
};
</script>
