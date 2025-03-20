import { httpClient } from './httpClients';

const loginEndpoint = '/login'

export const tokenService = {
   
   login: async (user) => {
      const payload = { 
         "username": user.username, 
         "password": user.password 
      }
      const res = await httpClient.post(loginEndpoint, payload);
      const token  = await res.data.access_token;
      localStorage.setItem('token', token);
      return token;
   },
   
   logout: () => {
      localStorage.removeItem('token');
   },
   
   getToken: () => {
      return localStorage.getItem('token');
   },
   
   isLoggedIn: () => {
      return !!localStorage.getItem('token');
   }
};