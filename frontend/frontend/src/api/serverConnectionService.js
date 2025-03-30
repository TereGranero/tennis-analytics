import { httpClient, httpAuthClient } from './httpClients';


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
   const res = await httpAuthClient.get(`${playersEndpoint}/edit/${id}`);
   return res.data;
};

export const getNamePlayers = async (fullnameToSearch = '') => {
   const res = await httpClient.get(`${playersEndpoint}/names`, {
      params: {
         search_fullname: fullnameToSearch, 
      }
   });
   return res.data;
};

export const createPlayer = async (player) => {
   const res = await httpAuthClient.post(playersEndpoint, player);
   return res.data;
};

export const updatePlayer = async (id, player) => {
   const res = await httpAuthClient.put(`${playersEndpoint}/${id}`, player);
   return res.data;
};

export const deletePlayer = async (id) => {
   const res = await httpAuthClient.delete(`${playersEndpoint}/${id}`);
   return res.data;
};



const rankingsEndpoint = '/rankings';

export const getEndYearRankings = async (page, perPage, yearToSearch = '2023') => {
   const res = await httpClient.get(`${rankingsEndpoint}/${yearToSearch}`, {
      params: {
         page: page, 
         per_page: perPage
      }
   });
return res.data;
};


const tournamentsEndpoint = '/tournaments';

export const getTournamentsByLevel = async (page, perPage, levelSlug = 'grand-slam') => {
   const res = await httpClient.get(`${tournamentsEndpoint}/level/${levelSlug}`, {
      params: {
         page: page, 
         per_page: perPage
      }
   });
return res.data;
};

export const getTournamentWinners = async (page, perPage, tourneySlug = 'roland_garros') => {
   const res = await httpClient.get(`${tournamentsEndpoint}/winners/${tourneySlug}`, {
      params: {
         page: page, 
         per_page: perPage
      }
   });
return res.data;
};

export const getRankingTitles = async (page, perPage, levelSlug = 'grand-slam') => {
   const res = await httpClient.get(`${tournamentsEndpoint}/titles/level/${levelSlug}`, {
      params: {
         page: page, 
         per_page: perPage
      }
   });
return res.data;
};

