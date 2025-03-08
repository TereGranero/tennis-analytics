import { httpClient } from './httpClient';


const playersEndpoint = '/players';

export const getAllPlayers = async (page, perPage, lastNameToSearch = '') => {
   const res = await httpClient.get(playersEndpoint, {
      params: {
         page: page, 
         per_page: perPage,
         search_name_last: lastNameToSearch
      }
   });
   return res.data;
};

export const getPlayerById = async (id) => {
   const res = await httpClient.get(`${playersEndpoint}/${id}`);
   return res.data;
};

export const getPlayerByIdForEditing = async (id) => {
   const res = await httpClient.get(`${playersEndpoint}/edit/${id}`);
   return res.data;
};

export const createPlayer = async (player) => {
   const res = await httpClient.post(playersEndpoint, player);
   return res.data;
};

export const updatePlayer = async (id, player) => {
   const res = await httpClient.put(`${playersEndpoint}/${id}`, player);
   return res.data;
};

export const deletePlayer = async (id) => {
   const res = await httpClient.delete(`${playersEndpoint}/${id}`);
   return res.data;
};



const rankingsEndpoint = 'rankings';

export const getEndYearRankings = async (page, perPage, yearToSearch = '2023') => {
   const res = await httpClient.get(rankingsEndpoint, {
      params: {
         page: page, 
         per_page: perPage,
         search_year: yearToSearch
      }
   });
return res.data;
};