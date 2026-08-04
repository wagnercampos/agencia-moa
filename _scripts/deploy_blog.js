// Deploy do BLOG da Agência MOA no cPanel `agenciamoa` (Home7/kessel3020) via WHM API (Fileman).
// Sobe: cria public_html/blog, envia os 5 artigos + index do blog, e atualiza os arquivos de raiz
// que mudaram (index.html com link Blog, sitemap.xml, llms.txt).
// Poucas chamadas, sequenciais, a UM endpoint (2087) — no padrão dos deploys anteriores da MOA.
const https = require('https');
const fs = require('fs');
const path = require('path');

const ENV = '/Users/wagnercampos/Documents/Gestor Turbo Cloud/.env';
function envVal(key) {
  const line = fs.readFileSync(ENV, 'utf8').split('\n').find(l => l.startsWith(key + '='));
  return line ? line.slice(key.length + 1).replace(/[\r\n]/g, '') : '';
}
const HOST = envVal('WHM_HOME7_HOST');
const USER = envVal('WHM_HOME7_USER');
const TOKEN = envVal('WHM_HOME7_TOKEN');
const CPUSER = 'agenciamoa';
const SITE = '/Users/wagnercampos/Documents/Criador de Sites/agencia-moa';

function whmPost(params) {
  return new Promise((resolve, reject) => {
    const body = new URLSearchParams(params).toString();
    const req = https.request({
      hostname: HOST, port: 2087, path: '/json-api/cpanel', method: 'POST',
      headers: {
        'Authorization': `whm ${USER}:${TOKEN}`,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(body),
      },
      rejectUnauthorized: false, timeout: 45000,
    }, (res) => {
      let data = ''; res.on('data', c => data += c);
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch { reject(new Error('resposta inválida: ' + data.slice(0, 200))); } });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.write(body); req.end();
  });
}
async function listDirs(dir) {
  const res = await whmPost({ cpanel_jsonapi_user: CPUSER, cpanel_jsonapi_apiversion: 3,
    cpanel_jsonapi_module: 'Fileman', cpanel_jsonapi_func: 'list_files', dir, types: 'dir' });
  const items = (res.result && res.result.data) || [];
  return new Set(items.map(i => i.file || i.name));
}
async function mkdir(parent, name) {
  // Fileman API3 não tem mkdir; API2 tem (params: path=pai, name=nova pasta).
  const res = await whmPost({ cpanel_jsonapi_user: CPUSER, cpanel_jsonapi_apiversion: 2,
    cpanel_jsonapi_module: 'Fileman', cpanel_jsonapi_func: 'mkdir', path: parent, name });
  const evt = (res.cpanelresult && res.cpanelresult.event) || {};
  if (res.cpanelresult && res.cpanelresult.error) throw new Error('mkdir ' + name + ': ' + res.cpanelresult.error);
  if (evt.result !== undefined && Number(evt.result) !== 1) throw new Error('mkdir ' + name + ': result ' + evt.result);
  return true;
}
async function saveFile(remoteDir, localPath, name) {
  const content = fs.readFileSync(localPath, 'utf8');
  const res = await whmPost({ cpanel_jsonapi_user: CPUSER, cpanel_jsonapi_apiversion: 3,
    cpanel_jsonapi_module: 'Fileman', cpanel_jsonapi_func: 'save_file_content',
    dir: remoteDir, file: name, content });
  const r = res.result || {};
  if (r.errors && r.errors.length) throw new Error(name + ': ' + JSON.stringify(r.errors));
  if (r.status !== undefined && r.status !== 1) throw new Error(name + ': status ' + r.status + ' ' + JSON.stringify(r.errors));
  return true;
}

const BLOG_FILES = ['index.html','negocio-nao-aparece-no-google-maps.html','quanto-custa-google-ads.html',
  'vale-a-pena-agencia-de-trafego.html','como-otimizar-google-meu-negocio.html'];
const ROOT_FILES = ['index.html','sitemap.xml','llms.txt'];

(async () => {
  console.log('== 1) conferindo public_html ==');
  const top = await listDirs('public_html');
  console.log('   pasta blog existe?', top.has('blog') ? 'sim' : 'não');
  if (!top.has('blog')) { console.log('== 2) criando public_html/blog =='); await mkdir('public_html', 'blog'); }
  console.log('== 3) subindo artigos do blog ==');
  for (const f of BLOG_FILES) { await saveFile('public_html/blog', path.join(SITE, 'blog', f), f); console.log('   OK  blog/' + f); }
  console.log('== 4) atualizando raiz (index/sitemap/llms) ==');
  for (const f of ROOT_FILES) { await saveFile('public_html', path.join(SITE, f), f); console.log('   OK  ' + f); }
  console.log('== FEITO ==');
})().catch(e => { console.error('FALHOU:', e.message); process.exit(1); });
