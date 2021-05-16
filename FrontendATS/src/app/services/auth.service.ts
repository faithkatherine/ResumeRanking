import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';



@Injectable({
  providedIn: 'root'
})
export class AuthService {
  auth_url:string = 'http://localhost:8000/api/account';
  jsonHeader = {headers: new HttpHeaders({'Content-Type':  'application/json'})};
  constructor(private httpClient: HttpClient, private router: Router) { }

  getAccessToken(){
    return localStorage.getItem('user_access_token');
  }

  signUp(email:string, username:string, password:string, password2:string){
    return this.httpClient.post(
      this.auth_url + '/register',
      // body content - required args can be seen in the Busywork function
      { 'email'   : email,
        'username': username,
        'password': password,
        'password2': password2
      },
      this.jsonHeader
    );
  }

  signIn(email:string, password:string){
    return this.httpClient.post(
      this.auth_url + '/login',
      // body args
      {
        'email': email,
        'password': password
      },
      this.jsonHeader
    ).subscribe(
      (result:any) => {
        // save the access token in local storage
        localStorage.setItem('user_access_token', result['token']);
        // save the user id in local storage
        //localStorage.setItem('user_id', result['user_id']);
        // change route to the profile component
        this.router.navigate(['account']);
      }
    )
  }

  signOut(){
    return this.httpClient.post(
      this.auth_url + '/logout',
      {},
      this.jsonHeader
    ).subscribe(
      (result:any) => {
        this.router.navigate(['registration']);
      }
    )
  }
}
