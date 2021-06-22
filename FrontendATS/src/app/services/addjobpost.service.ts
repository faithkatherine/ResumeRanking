import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { AddJobPostComponent } from '../add-job-post/add-job-post.component';

@Injectable({
  providedIn: 'root'
})
export class AddjobpostService {

  auth_url:string = 'http://localhost:8000/api/jobs';


  jsonHeader = {headers: new HttpHeaders()};
  constructor(private httpClient: HttpClient, private router: Router, addjob:AddJobPostComponent) { }

  addJob(FormData){
    return this.httpClient.post(
      this.auth_url + '/create/',
      // body content - required args can be seen in the Busywork function
      /*{ 'title': title,
        'body': body,
        'image': image
      },*/
      FormData,
      this.jsonHeader
    ).subscribe(
      (response:any) => {
        console.log(response);
      })
  }
}
