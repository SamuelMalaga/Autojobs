const pup = require('puppeteer');
const sqlite3 = require('sqlite3').verbose();
const yargs = require('yargs');
const fs = require('fs');
const { error } = require('console');

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

function delayTime(time) {
  return new Promise(function(resolve) {
    setTimeout(resolve, time);
  });
}

async function scrollToEnd(page) {
  let previousHeight = 0;

  await page.evaluate(() => {
    window.scrollBy(0, window.innerHeight);
  });

  await delayTime(1000); // Espera 4 segundos.

  const newHeight = await page.evaluate(() => {
    return document.body.scrollHeight;
  });

  const successAlert = await page.evaluate(() => {
    const alertDiv = document.querySelector('div[role="alert"][type="success"]');
    return alertDiv ? alertDiv.classList.contains('hidden') : false;
  });

  if (!successAlert) {
      console.log('A div de alerta de sucesso não está mais oculta. Encerrando a execução.');
      return true;
    }

  // Tente clicar no botão "Ver mais vagas" com tratamento de erro.
  try {
    await page.click('button[aria-label="Ver mais vagas"]');
  } catch (error) {

  }

  return false; // A página ainda não atingiu o final.
}
async function extractDataFromPage(page) {
  const data = await page.evaluate(() => {
    const items = [];
    const xpath = '//*[@id="main-content"]/section[2]/ul/li/div';
    const iterator = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

    for (let i = 0; i < iterator.snapshotLength; i++) {
      const item = iterator.snapshotItem(i);
      const dataEntityUrn = item.getAttribute('data-entity-urn');
      items.push({
        JobId: dataEntityUrn.match(/\d+$/)[0],
        JobTitle:"",
        JobDescription:""
       });
    }

    return items;
  });

  return data;
}
async function saveDataToJSON(data, filename) {
  try {
    const jsonData = JSON.stringify(data, null, 2); // Converte os dados em formato JSON com recuo de 2 espaços.
    fs.writeFileSync(filename, jsonData); // Salva os dados em um arquivo JSON.

    console.log(`Dados salvos em ${filename}`);
  } catch (error) {
    console.error('Erro ao salvar os dados em JSON:', error);
  }
}
async function saveDataToSQLite(data) {
  const db = new sqlite3.Database('jobs.db');
  db.serialize(() => {
    db.run('BEGIN TRANSACTION');

    const stmt = db.prepare('INSERT INTO jobs (jobId, title, description) VALUES (?, ?, ?)');

    for (const item of data) {
      stmt.run(item.JobId, item.JobTitle, item.JobDescription);
    }

    stmt.finalize();
    db.run('COMMIT');
  });

  db.close();
}

async function findAllChildrenByXpath(page, xpathString){
  return page.$x(xpathString)
}

async function findChildByXpath(page, xpathString){
  return page.$x(xpathString)
}
/**
 * Obtém o valor de uma propriedade de um elemento HTML usando um XPath.
 * @param {string} xpath - A expressão XPath para localizar o elemento na página.
 * @param {string} propriedade - O nome da propriedade que você deseja obter do elemento.
 * @returns {string | null} - O valor da propriedade, ou null se o elemento não for encontrado.
 */
async function getPropertyByXpath(page, xpath, propriedade) {
  try {
    const elemento = await page.waitForXPath(xpath); // Substitua "page" pela sua referência à página.

    if (elemento) {
      const valor = await elemento.evaluate((element, prop) => {
        return element.getAttribute(prop);
      }, propriedade);

      return valor || null;
    } else {
      return null;
    }
  } catch (error) {
    console.error('Erro ao obter propriedade por XPath:', error);
    return null;
  }
}
async function isDescriptionValid(list, currentIndex){
  //let previousIndex = currentIndex -1;
  let previousText = list[currentIndex].job_description;
  let currentText = list[currentIndex+1]
  if (previousText !== null && currentText === previousText) {
    return true;
  };
  return false;
}
/**
 * Insere os objetos job em uma tabela SQLite.
 * @param {string} databaseName - O nome do banco de dados SQLite.
 * @param {Array} jobs - Um array de objetos job a serem inseridos na tabela.
 */
async function insertJobsIntoDatabase(databaseName, jobs) {
  const db = new sqlite3.Database(databaseName);

  const insertJobQuery = `
      INSERT INTO jobs (job_id, job_title, company_name, job_link, job_description, double_Check)
      VALUES (?, ?, ?, ?, ?, ?);
  `;

  jobs.forEach((job) => {
      db.run(insertJobQuery, [
          job.job_id,
          job.job_title,
          job.company_name,
          job.job_link,
          job.job_description,
          job.double_Check
      ], (err) => {
          if (!err) {
              console.log(`Inserido(veio do jobs): ${job.job_title}`);
          } else {
              console.error(`Erro ao inserir ${job.job_title}: ${err.message}`);
          }
      });
  });

  db.close();
}
async function getPropertyWithFallback(page, xpath, property, maxRetries) {
  let retries = 0;
  let result = null;

  while (retries < maxRetries) {
    try {
      const element = await page.waitForXPath(xpath);
      result = await element.evaluate((el, prop) => el.getAttribute(prop), property);
      break; // Se tiver sucesso, saia do loop.
    } catch (error) {
      console.error(`Erro ao obter ${property} - Tentativa ${retries + 1}`);
      retries++;
    }
  }

  return result;
}
async function getTextContentByXPath(page, xpath) {
  try {
    const element = await page.waitForXPath(xpath);
    return element ? await element.evaluate(element => element.textContent) : null;
  } catch (error) {
    console.error(`Erro ao obter texto do XPath '${xpath}': ${error.message}`);
    return null;
  }
}

async function parseLiItems(page, maxItens) {
  let itensColetados = 0;
  const resultados = new Array();

  while (itensColetados < maxItens) {
    // Realize as operações que deseja no elemento, como extrair informações e adicionar aos resultados.
    //Index in the <ul> starting point is 1
    const numberOfLis = await findAllChildrenByXpath(page, '//*[@id="main-content"]/section[2]/ul/li')
    liIndex = itensColetados + 1
    //
    console.log('valor LIiNDEX' ,liIndex)
    if(liIndex === numberOfLis.length){
      break
    }

    //Extrai os dados da anchor tag
    const aTagXpath = `//*[@id="main-content"]/section[2]/ul/li[${liIndex}]/div/a`
    const anchorTagToClick = await page.waitForXPath(aTagXpath)
    const testPropertie = 'href'
    const jobLink = await getPropertyWithFallback(page, aTagXpath, 'href', 3);
    //const jobLink = await getPropertyByXpath(page, aTagXpath, 'href');
    //Pega o nome da vaga
    const h3TagXpath = `//*[@id="main-content"]/section[2]/ul/li[${liIndex}]/div/div[2]/h3`;
    const h3TagInstance = await page.waitForXPath(h3TagXpath)
    const jobTitle = await getTextContentByXPath(page, h3TagXpath);
    //await h3TagInstance.evaluate(element => element.textContent);
    //Pega o nome da empresa
    const companyNameTagXpath =`//*[@id="main-content"]/section[2]/ul/li[${liIndex}]/div/div[2]/h4`
    const companyNameTag = await page.waitForXPath(companyNameTagXpath)
    const companyName = await getTextContentByXPath(page, companyNameTagXpath);
    //await companyNameTag.evaluate(element => element.textContent);
    //Pega o texto principal da descrição
    await page.waitForSelector('.decorated-job-posting__details');
    const jobInfoDivXpath='/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div'
    const jobDescription = await getTextContentByXPath(page, jobInfoDivXpath);
    //const jobInfoDiv = await page.$('.decorated-job-posting__details');
    //const jobDescription = await jobInfoDiv.evaluate(element => element.textContent);

    //Pega a propriedade da div que contém o ID da vaga
    const jobIdDivXpath=`/html/body/div[1]/div/main/section[2]/ul/li[${liIndex}]/div`
    const jobIdDiv = await page.waitForXPath(jobIdDivXpath)
    const dataEntityUrn = await getPropertyByXpath(page, jobIdDivXpath, 'data-entity-urn');
    const jobId = dataEntityUrn.match(/\d+$/)[0] ? dataEntityUrn.match(/\d+$/)[0] : null;
    job = {
      "job_id":jobId,
      "job_title":jobTitle,
      "company_name":companyName,
      "job_link": jobLink,
      "job_description": jobDescription,
      "double_Check": null
    }
    resultados.push(job)

    await anchorTagToClick.click()

    try {
      await page.click('button[aria-label="Ver mais vagas"]');
      console.log('achou o button')
    } catch (error) {
      console.log('não achou o button')
    }

    //const randomDelay = Math.floor(Math.random() * (10000 - 8000 + 1)) + 8000;
    await delayTime(10000)

    // Aumente o contador de itens coletados.
    itensColetados++;
  }

  return resultados; // Os resultados podem ser armazenados em um array ou outro formato desejado.
}
async function cleanUpParsedResults(parsedResults) {
  // Inicialize o valor do job_description anterior
  //let previousJobDescription = '';

  // Função para tratar o campo job_id
  function parseJobId(jobId) {
    // Tenta converter o texto em um número inteiro
    const jobIdNumber = parseInt(jobId, 10);
    // Verifica se a conversão foi bem-sucedida
    if (!isNaN(jobIdNumber)) {
      return jobIdNumber;
    }
    // Se a conversão falhar, retorne null ou outra ação desejada
    return null;
  }

  // Função para limpar texto (remover \n e espaços em branco)
  function cleanText(text) {
    if (text !== null) {
      text = text.replace(/\n/g, '').replace(/\s+/g, ' ').trim();

      console.log('veio do cleantext',text)
      return text
    } else {
      // Lida com o caso em que 'text' é nulo, se necessário.
      return null
    }
  }

  // Limpe o primeiro item do array, pois não há item anterior a ele
  parsedResults[0].job_id = parseInt(parsedResults[0].job_id, 10);
  parsedResults[0].job_title = cleanText(parsedResults[0].job_title);
  parsedResults[0].company_name = cleanText(parsedResults[0].company_name);
  parsedResults[0].job_description = cleanText(parsedResults[0].job_description);
  parsedResults[0].double_Check = false;

  for (let i = 1; i < parsedResults.length; i++) {
    const currentJob = parsedResults[i];
    const previousJob = parsedResults[i - 1];

    // Trate o campo job_id
    currentJob.job_id = parseInt(currentJob.job_id, 10);

    // Limpe os campos de texto
    currentJob.job_title = cleanText(currentJob.job_title);
    currentJob.company_name = cleanText(currentJob.company_name);
    currentJob.job_description = cleanText(currentJob.job_description);

    // Verifique se job_description é igual ao anterior e defina double_Check
    currentJob.double_Check = currentJob.job_description === previousJob.job_description;
  }


  return parsedResults;
}


(async () => {
  const startTime = new Date();
  console.log(`Iniciando scraping em ${startTime.getHours()}:${startTime.getMinutes()}:${startTime.getSeconds()}`)
  const browser = await pup.launch();
  const page = await browser.newPage();

  const jobName = encodeURIComponent(argv['job-name']);
  const jobLocation = encodeURIComponent(argv['job-location']);
  const jobType = encodeURIComponent(argv['job-type']);

  // Defina o tamanho da tela visível, por exemplo, 1200x800 pixels
  await page.setViewport({ width: 1359, height: 947 });

  await page.goto(`https://www.linkedin.com/jobs/search?keywords=${jobName}&location=${jobLocation}&f_WT=${jobType}`);

  const data = []; // Lista para armazenar as informações
  const limit = 1000; // Limite de registros

  const ulXPathSelector = await findAllChildrenByXpath(page, '//*[@id="main-content"]/section[2]/ul/li')

  const rawOutput = await parseLiItems(page, 200);

  console.log('Jobs coletados',rawOutput.length);

  const cleanedOutput = await cleanUpParsedResults(rawOutput);

  //console.log(cleanedOutput)

  await insertJobsIntoDatabase('autojobs.db',cleanedOutput )

  //console.log(cleanedOutput)


  const endTime = new Date();
  console.log(`Encerrando scraping em ${endTime.getHours()}:${endTime.getMinutes()}:${endTime.getSeconds()}`)
  await browser.close();


})();
