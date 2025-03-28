import { httpClientWikiData } from './httpClients';
import { getImageAttribution } from './wikiCommonsConnectionService';

const wikiDataEndpoint = '/w/api.php';


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

         const imageAttribution = await getImageAttribution(fileName);

         return { imageUrl, imageAttribution };
      }

   console.log('Image URL no encontrada');
   return null;
};

export const getWikiDataId = async (name) => {
   console.log(`Requesting to WikiData for ${name} Id...`);
   const res = await httpClientWikiData.get(wikiDataEndpoint, {
      params: {
         action: 'wbsearchentities',
         format: 'json',
         language: 'en',
         search: name,
         type: 'item',
         limit: 5,
         props: 'claims|descriptions',
         origin: '*'
      },
   });

   const tournament = res.data.search.find(item => {
      const isTennisTournamentInstance = item.claims?.P31?.some(claim => 
         ['Q300007', 'Q13219666'].includes(claim.mainsnak.datavalue?.value.id)
      );
      const isTennisDescription = item.description?.toLowerCase().includes('tennis');

      return isTennisTournamentInstance || isTennisDescription;
   });

   if (tournament) {
      console.log(`Wikidata_id encontrado: ${tournament.id}`)
      return tournament.id;
    }

   console.log('Wikidata_id no encontrado')
   return null;
};

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
      
      const imageAttribution = await getImageAttribution(fileName);

      return { logoUrl, imageAttribution };
   }
   console.log('Logo URL no encontrada');
   return null;
};
