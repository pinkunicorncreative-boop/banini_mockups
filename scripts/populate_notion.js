const fs = require('fs');
const https = require('https');

const NOTION_KEY = fs.readFileSync('/Users/krazeerastagroup/.config/notion/api_key', 'utf8').trim();
const DATABASE_ID = '32a99e91-5cba-817b-89a4-d24c85e6429d';

const roster = [
  { name: 'Marcia Bennett', role: 'Anchor Council (AC)' },
  { name: 'Marcus Kerridge', role: 'Anchor Council (AC)' },
  { name: 'Danielle Grant', role: 'Anchor Council (AC)' },
  { name: 'Arjun Naidoo', role: 'High-Fashion Authority (HF)' },
  { name: 'Priya Singh', role: 'High-Fashion Authority (HF)' },
  { name: 'Liam Chin', role: 'High-Fashion Authority (HF)' },
  { name: 'Amara Chen-Williams', role: 'High-Fashion Authority (HF)' },
  { name: 'Kai Morgan', role: 'Editorial Division (ED)' },
  { name: 'Asha Ravindra', role: 'Editorial Division (ED)' },
  { name: 'Solange Campbell-Kim', role: 'Editorial Division (ED)' },
  { name: 'Rashaad Beckford-Johnson', role: 'Editorial Division (ED)' },
  { name: 'Helena Ribeiro-James', role: 'Editorial Division (ED)' },
  { name: 'Ade Marquez', role: 'Editorial Division (ED)' },
  { name: 'Samantha Jones', role: 'Narrative Canon (T01 Inheritor)' },
  { name: 'Mavis Elaine Jones', role: 'Narrative Artifact (T01 Grandmother)' }
];

async function insertPerson(person) {
  const data = JSON.stringify({
    parent: { database_id: DATABASE_ID },
    properties: {
      'Character/Name': { title: [{ text: { content: person.name } }] },
      'Brand Affinity': { select: { name: 'Jamrock' } },
      'Status': { select: { name: person.name.includes('Mavis') ? 'Artifact/Prop' : 'Active Canon' } },
      'Archetype/Role': { rich_text: [{ text: { content: person.role } }] }
    }
  });

  const options = {
    hostname: 'api.notion.com',
    path: '/v1/pages',
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${NOTION_KEY}`,
      'Notion-Version': '2025-09-03',
      'Content-Type': 'application/json',
      'Content-Length': data.length
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let responseBody = '';
      res.on('data', chunk => responseBody += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          console.log(`Success: ${person.name}`);
          resolve();
        } else {
          console.error(`Error for ${person.name}: ${res.statusCode} ${responseBody}`);
          resolve(); // Resolve anyway to keep going
        }
      });
    });
    req.on('error', (e) => reject(e));
    req.write(data);
    req.end();
  });
}

async function run() {
  for (const person of roster) {
    await insertPerson(person);
    // Add a slight delay to avoid rate limits
    await new Promise(r => setTimeout(r, 400));
  }
}

run();
