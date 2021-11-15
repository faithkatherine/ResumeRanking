import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ResumePostService {

  private list_blog_url:string = 'http://localhost:8000/api/resumes/list/';
  constructor(private httpClient: HttpClient) { }
  list() {
    return this.httpClient.get(this.list_blog_url);
  }

}
