import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, FormBuilder, Validators} from '@angular/forms';
//import {AddjobpostService} from '../services/addjobpost.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-add-job-post',
  templateUrl: './add-job-post.component.html',
  styleUrls: ['./add-job-post.component.css']
})
export class AddJobPostComponent implements OnInit {
  auth_url:string = 'http://localhost:8000/api/jobs';

  form: FormGroup;
  jsonHeader = {headers: new HttpHeaders()};
  constructor(private fb: FormBuilder, private httpClient: HttpClient, private router: Router) {
    this.form = this.fb.group({
      title: [''],
      body: [''],
      image: [null]
    });
  }

  uploadFile(event) {
    const file = (event.target as HTMLInputElement).files[0];
    this.form.patchValue({
      image: file
    });
    this.form.get('image').updateValueAndValidity()
  }

  addJobPost(){
    const formData = new FormData();
    formData.append( 'title', this.form.get('title').value);
    formData.append( 'body', this.form.get('body').value);
    formData.append( 'image', this.form.get('image').value);

    this.httpClient.post(
      this.auth_url + '/create/',
      formData,
      this.jsonHeader
    ).subscribe(
      (response:any) => {
        console.log(response);
      })
      this.router.navigate(['/account']);

  }

  ngOnInit(): void {
  }


}
