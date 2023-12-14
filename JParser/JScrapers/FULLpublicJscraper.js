const pup = require('puppeteer');
const sqlite3 = require('sqlite3').verbose();
const yargs = require('yargs');


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
    },
    'upper-limit': {
      describe:'How much jobs you want the scraper to search, 1000 is the theoretical limit but 200 is the max recommended',
      demandOption: false, // Defina como true se o argumento for obrigatório
      type: 'int', // Especifique o tipo do argumento (string neste caso)
    }
  })
  .argv;

function delayTime(time) {
  return new Promise(function(resolve) {
    setTimeout(resolve, time);
  });
}
async function findAllChildrenByXpath(page, xpathString){
  return page.$x(xpathString)
}
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
    return null;
  }
}
async function insertJobsIntoDatabase(databaseName, jobs) {
  const db = new sqlite3.Database(databaseName);

  const insertJobQuery = `
      INSERT INTO JobsAPI_job (job_id, job_title, company_name, job_link, job_description, double_check, source)
      VALUES (?, ?, ?, ?, ?, ?, ?);
  `;

  jobs.forEach((job) => {
      db.run(insertJobQuery, [
          job.job_id,
          job.job_title,
          job.company_name,
          job.job_link,
          job.job_description,
          job.double_Check,
          "linkedin"
      ], (err) => {
          if (!err) {
          } else {
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
    } catch (error) {
    }

    //const randomDelay = Math.floor(Math.random() * (10000 - 8000 + 1)) + 8000;
    await delayTime(6000)

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

  const browser = await pup.launch(
    {
      headless:false,
      args: ['--lang=en-US']
    });
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


  const cleanedOutput = await cleanUpParsedResults(rawOutput);

  await insertJobsIntoDatabase('C:/Users/SamuelMendesMalaga/Documents/Autojobs/SQLiteDB/autojobs.db',cleanedOutput )

  const endTime = new Date();

  await browser.close();


})();
