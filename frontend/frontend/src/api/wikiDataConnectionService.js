import { httpClientWikiData } from './httpClients';
import { getImageAttribution } from './wikiCommonsConnectionService';
import { cleanAttribution } from '@/services/attribution_services';

// Connects to Wikidata

const wikiDataEndpoint = '/w/api.php';

// Retrieves image for a provided Wikidata entity ID
export const getWikiDataImage = async (wikidata_id) => {
   console.log('Requesting to WikiData for image...');
   const res = await httpClientWikiData.get(wikiDataEndpoint, {
      params: {
         action: 'wbgetclaims',
         format: 'json',
         origin: '*',
         entity: wikidata_id,
         property: 'P18'
      },
   });

   const fileName = res.data.claims?.P18?.[0]?.mainsnak?.datavalue?.value;
   if (fileName) {
      const imageUrl = `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(fileName)}`;
      console.log(`Image URL: ${imageUrl}`);

      let imageAttribution = await getImageAttribution(fileName);
      imageAttribution = cleanAttribution(imageAttribution)

      return { imageUrl, imageAttribution };
   }

   console.log('Image URL no encontrada');
   return null;
};

// Searches Wikidata entity ID for a tournament name
// In the future, try to query Wikimedia Commons too
export const getWikiDataId = async (name) => {
   console.log(`Requesting to WikiData for ${name} Id...`);
   const nameLow = name.toLowerCase();
   const query = ( nameLow.includes('open') || nameLow.includes('masters') || nameLow.includes('roland') || nameLow.includes('wimbledon') )? name : `${name} open`;
   const res = await httpClientWikiData.get(wikiDataEndpoint, {
      params: {
         action: 'wbsearchentities',
         format: 'json',
         language: 'en',
         search: query,
         type: 'item',
         limit: 5,
         origin: '*'
      },
   });

   // Verifies it is a tennis tournament
   const tournament = res.data.search.find(item => {
      const isTennisDescription = item.description?.toLowerCase().includes('tennis');
      return isTennisDescription;
      });
      
      if (tournament) {
      console.log(`Wikidata_id encontrado: ${tournament.id}`)
      return tournament.id;
      }
      
      console.log('Wikidata_id no encontrado')
      return null;
};


// Retrieves all claims of an entity for a provided Wikidata ID and searches logo in images properties
export const getWikiDataLogo = async (wikidata_id) => {
   console.log('Requesting to WikiData for logo...');
   const res = await httpClientWikiData.get(wikiDataEndpoint, {
      params: {
         action: 'wbgetentities',
         ids: wikidata_id,
         format: 'json',
         props: 'claims',
         origin: '*'
      },
   });

   const entity = res.data.entities[wikidata_id];

   const imageProperties = ['P154', 'P2910', 'P18']; // Logo, image, icon
   let fileName;

   for (const property of imageProperties) {
      fileName = entity?.claims?.[property]?.[0]?.mainsnak?.datavalue?.value;
      if (fileName) {
         break;
      }
   }
    
   if (fileName) {

      const logoUrl = `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(fileName)}`;
      console.log(`Logo URL: ${logoUrl}`);
      
      let imageAttribution = await getImageAttribution(fileName);
      imageAttribution = cleanAttribution(imageAttribution)

      return {logoUrl, imageAttribution };
   }
   console.log('Logo URL no encontrada');
   return null;
};
