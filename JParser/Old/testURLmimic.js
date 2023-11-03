const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const yargs = require('yargs');
// URL da página da web https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Remote%2BSoftware%2BEngineer&location=Brazil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=500&original_referer=&start=25
// URL da página da web
const argv = yargs
  .options({
    'job-name': {
      describe: 'Nome do trabalho',
      demandOption: true, // Defina como true se o argumento for obrigatório
      type: 'string', // Especifique o tipo do argumento (string neste caso)
    },
    'job-location': {
      describe: 'Localização do trabalho',
      demandOption: true, // Defina como true se o argumento for obrigatório
      type: 'string', // Especifique o tipo do argumento (string neste caso)
    },
    'job-type': {
      describe:'Tipo de trabalho, Presencial (1), Híbrido (2) ou remoto (3)',
      demandOption: true, // Defina como true se o argumento for obrigatório
      type: 'int', // Especifique o tipo do argumento (string neste caso)
    }
  })
  .argv;


const fetchHTMLContent = (url) => {
  // Faz uma requisição para obter o conteúdo da página
  return fetch(url)
    .then((response) => {
      // Verifica se a resposta da requisição foi bem-sucedida (código de status 200)
      if (!response.ok) {
        throw new Error(`Erro na requisição: ${response.status}`);
      }

      // Lê o conteúdo da resposta como texto
      return response.text();
    })
    .then((htmlContent) => {
      // Retorna o documento DOM criado a partir do conteúdo HTML
      return new JSDOM(htmlContent).window.document;
    });
};

const extractDataFromDocument = (doc) => {
  // Use document.querySelectorAll para selecionar todas as <li> com a propriedade data-entity-urn
  const liElements = doc.querySelectorAll('li');
  const data = [];

  // Itere pelas li's
  liElements.forEach((li) => {
    // Selecione a <div> filha dentro do <li>.
    const divElement = li.querySelector('div');

    // Verifique se a <div> foi encontrada.
    if (divElement) {
      // Obtenha o valor da propriedade 'data-entity-urn'.
      const dataEntityUrn = divElement.getAttribute('data-entity-urn');
      const anchorElement = divElement.querySelector('a');

      // Verifique se o elemento <a> foi encontrado
      if (anchorElement) {
        // Obtenha o valor do atributo href
        const hrefValue = anchorElement.getAttribute('href');
        data.push({ JobId: dataEntityUrn.match(/\d+$/)[0], JobLink: hrefValue });
      } else {
        console.log('Elemento <a> não encontrado dentro da div.');
      }
    } else {
      console.log('Nenhuma <div> encontrada no <li>.');
    }
  });

  return data;
};

function saveJSON(array, fileName) {
  // Converte o array em uma string JSON
  const json = JSON.stringify(array, null, 2);

  // Escreve a string JSON no arquivo
  fs.writeFileSync(fileName, json, 'utf-8');

  console.log(`Os dados foram salvos em ${fileName}`);
}
//&position=1&pageNum=0&start=25
function getAllJobs(initialURL){
  const pageNumParam = '&position=1&pageNum=0'
  const stepSize = 25
  let pageItemCount = 0
  for(let i=0; i < 4;i++){
    var pageStart = `&pageStart=${i*stepSize}`
    let completeURLToIterate = `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Remote%2BSoftware%2BEngineer&location=Brazil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=500&original_referer=${pageStart}`
    console.log(completeURLToIterate)
  }
}

// Exemplo de uso:
const jobName = encodeURIComponent(argv['job-name']);
const jobLocation=encodeURIComponent(argv['job-location']);
const jobType=encodeURIComponent(argv['job-type']);
//https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Remote%2BSoftware%2BEngineer&location=Brazil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=500&original_referer=&start=25
const url = `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=${jobName}&location=${jobLocation}&f_WT=${jobType}`;


getAllJobs(url);


// fetchHTMLContent(url)
//   .then((doc) => {
//     const extractedPageData = extractDataFromDocument(doc);
//     console.log(extractedPageData);
//   })
//   .catch((error) => {
//     console.error('Erro:', error);
//   });

