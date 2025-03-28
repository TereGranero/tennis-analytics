import { httpClientWikiCommons } from './httpClients';

const wikiCommonsEndpoint = '/w/api.php';

export const getWikiCommonsImage = async (query) => {
   console.log('Requesting to WikiCommons for image...');
   const res = await httpClientWikiCommons.get(wikiCommonsEndpoint, {
      params: {
         action: 'query',
         format: 'json',
         list: 'search',
         srsearch: `${query} filetype:jpg`,  // only images
         srnamespace: 6,  // only files
         srlimit: 1,       // 1 result
         origin: '*'      // CORS
      },
   });

   if (res.data.query?.search?.length > 0) {
      const imageTitle = res.data.query.search[0].title;
      const imageUrl = `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(imageTitle)}`;
      console.log(`URL: ${imageUrl}`);

      const fileName = imageTitle.replace(/^File:/, '');
      const imageAttribution = await getImageAttribution(fileName);

      return { imageUrl, imageAttribution };
   }
   console.log('Image URL no encontrada');
   return null;
};


export const getImageAttribution = async (fileName) => {
   console.log(`Requesting to WikiCommons for attribution...`);
   const res = await httpClientWikiCommons.get(wikiCommonsEndpoint, {
      params: {
         action: 'query',
         format: 'json',
         titles: `File:${fileName}`,
         prop: 'imageinfo',
         iiprop: 'url|extmetadata',
         origin: '*'
      },
   });

   const pages = res.data.query?.pages;
   //console.log('API Response:', JSON.stringify(res.data, null, 2));
   const imageInfo = Object.values(pages)[0]?.imageinfo?.[0];

   if (imageInfo) {
      const metadata = imageInfo.extmetadata;
      const title = metadata?.ObjectName?.value || '';
      const author = metadata?.Artist?.value || '';
      const license = metadata?.LicenseShortName?.value || '';
      const licenseUrl = metadata?.LicenseUrl?.value || '#';
      const description = metadata?.ImageDescription?.value || '';

      return {
         title,
         author,
         license,
         licenseUrl,
         description,
         filePageUrl: imageInfo.descriptionurl // Commons url
      };
   }

   return null;
};


